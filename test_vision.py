import base64
import mimetypes
import io
from pathlib import Path
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import pypdfium2 as pdfium

def encode_file(file_path: str) -> list[tuple[str, str]]:
    """Encodes a file (image or PDF) to a list of (mime_type, base64_string) tuples."""
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types/Common_types
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "image/jpeg"  # Default fallback

    if mime_type == "application/pdf":
        pdf = pdfium.PdfDocument(file_path)
        encoded_images = []

        for i in range(len(pdf)):
            page = pdf[i]

            # scale=2 provides higher resolution (e.g. 144 DPI) often better for Vision models
            pil_image = page.render(scale=2).to_pil()

            buffered = io.BytesIO()
            pil_image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            encoded_images.append(("image/jpeg", img_str))

        return encoded_images
    
    elif mime_type.startswith("image"):
        with open(file_path, "rb") as file:
            return [(mime_type, base64.b64encode(file.read()).decode("utf-8"))]
    
    else:
        raise ValueError(f"file type {mime_type} is not supported, please provide image of pdf")

def main():
    file_path = "path/to/your/image_or_pdf_file"  # Update this path to your file
    file_path = str(Path(file_path).expanduser().resolve())

    if not Path(file_path).exists():
        print(f"Please update the 'file_path' variable in the script to point to a valid file.")
        return

    try:
        encoded_files = encode_file(file_path)

        content_list = [
            {
                "type": "text",
                "text": "Describe what is in this file."
            }
        ]

        for mime_type, base64_data in encoded_files:
            content_list.append({
                "type": "image_url",
                "image_url": f"data:{mime_type};base64,{base64_data}"
            })

        message = HumanMessage(content=content_list) # type: ignore

        llm = ChatOllama(
            model="llava:13b",
            temperature=0,
            base_url="http://localhost:11434"
        )

        print("Analyzing file...")
        response = llm.invoke(input=[message])
        print("\nResponse:")
        print(response.content)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
