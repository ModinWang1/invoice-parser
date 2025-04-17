import os
from PIL import Image
import torch
from transformers import AutoModelForCausalLM
from deepseek_vl2.models import DeepseekVLV2Processor, DeepseekVLV2ForCausalLM
import torch.cuda.amp as amp
from deepseek_vl2.utils.io import load_pil_images
from huggingface_hub import snapshot_download

if torch.cuda.is_available():
    print("CUDA is available!")
    device = torch.device("cuda")  # Set device to CUDA
else:
    print("CUDA is NOT available.")
    device = torch.device("cpu")  # Set device to CPU (or raise an exception)

scaler = amp.GradScaler(enabled=torch.cuda.is_available())

MODEL_DIR = "./models/deepseek-vl2-tiny"

# Automatically download if model isn't found
if not os.path.exists(MODEL_DIR):
    print("🔽 Model not found locally. Downloading...")
    snapshot_download(
        repo_id="deepseek-ai/deepseek-vl2-tiny",
        local_dir=MODEL_DIR,
        repo_type="model"
    )
    print("✅ Model downloaded!")


vl_chat_processor: DeepseekVLV2Processor = DeepseekVLV2Processor.from_pretrained(MODEL_DIR)
tokenizer = vl_chat_processor.tokenizer

vl_gpt: DeepseekVLV2ForCausalLM = AutoModelForCausalLM.from_pretrained(MODEL_DIR, trust_remote_code=True)

vl_gpt = vl_gpt.to(torch.float16).cuda().eval()

# For testing
#image_path = './invoices_as_images/Home Depot 3082066_page_1.jpg'
#image_path = './invoices_as_images/3463_001_page_1.jpg'

#image_path = './invoices_as_images/Uber Stella 20240628.jpg'

#image_path = './invoices_as_images/Uber Receipt 20240903 - Cole_page_1.jpg'

prompt = (
    "You are a data extraction assistant.\n\n"
    "Task:\n"
    "Extract the following fields from the invoice or receipt image:\n"
    "- 'invoice_number': string ('N/A' if missing)\n"
    "- 'date': string in mm/dd/yyyy format ('N/A' if missing)\n"
    "- 'items': a list of dictionaries, each with 'name', 'quantity', and 'cost'\n"
    "- 'subtotal': number (0.0 if missing)\n"
    "- 'tax': number (0.0 if missing)\n"
    "- 'total': number (0.0 if missing)\n\n"
    "Only return a valid Python dictionary with **all** of these keys. No extra text.\n\n"
    "Example format (do not copy values):\n"
    "{\n"
    "  'invoice_number': <string>,\n"
    "  'date': <mm/dd/yyyy>,\n"
    "  'items': [{'name': <string>, 'quantity': <int>, 'cost': <float>}],\n"
    "  'subtotal': <float>,\n"
    "  'tax': <float>,\n"
    "  'total': <float>\n"
    "}\n\n"
    "Now extract the values from the current image. "
    "Keep in mind, if there is no quantity on an item it is assumed to be 1. "
    "Also keep in mind that tax can also be known as GST or HST. "
    "Also keep in mind that the 'total' is usually the largest amount and should at least be the same as the subtotal. "
    "Also keep in mind 'invoice number' can also be known as 'invoice #'"
)
def process_invoice(image_path: str, prompt: str) -> str:

    image = Image.open(image_path).convert('RGB')

    conversation = [
        {
            "role": "<|User|>",
            "content": f"<image>\n|ref|>{prompt}<|/ref|>.",
            "images": [image],
        },
        {"role": "<|Assistant|>", "content": ""},
    ]

    model_inputs = vl_chat_processor(
        conversations=conversation,
        images=[image],
        force_batchify=True,
        system_prompt=""
    ).to(vl_gpt.device)

    model_inputs.images = model_inputs.images.to(dtype=torch.float16)

    inputs_embeds = vl_gpt.prepare_inputs_embeds(**model_inputs)

    with torch.no_grad():
        outputs = vl_gpt.language.generate(
            inputs_embeds=inputs_embeds,
            attention_mask=model_inputs.attention_mask,
            pad_token_id=tokenizer.eos_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            max_new_tokens=4096,
            do_sample=False,
            use_cache=True
        )

    response = tokenizer.decode(outputs[0].tolist(), skip_special_tokens=True)
    print(response)
    return response

