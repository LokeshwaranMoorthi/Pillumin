from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,"prescription_analyzer/home.html")

from django.shortcuts import render
from doctr.models import ocr_predictor
from doctr.io import DocumentFile

# Load Doctr OCR model once at startup
model = ocr_predictor(pretrained=True)

# ⚠️ Simple conflict database
CONFLICT_DB = {
    ("paracetamol", "ibuprofen"): "May increase risk of stomach bleeding.",
    ("aspirin", "warfarin"): "Increases bleeding risk when combined.",
    ("amoxicillin", "methotrexate"): "May raise methotrexate levels to toxic levels.",
}


def check_conflicts(meds):
    meds = [m.lower() for m in meds]
    conflicts = []
    for i in range(len(meds)):
        for j in range(i + 1, len(meds)):
            pair = tuple(sorted((meds[i], meds[j])))
            if pair in CONFLICT_DB:
                conflicts.append({
                    "pair": pair,
                    "warning": CONFLICT_DB[pair]
                })
    return conflicts

# 🌟 Main view
def analyze_prescription(request):
    conflicts = []
    extracted_text = ""
    
    if request.method == "POST" and request.FILES.get("prescription"):
        uploaded_file = request.FILES["prescription"]
        try:
            # Let Doctr handle the image directly
            image = DocumentFile.from_images(uploaded_file)
            result = model(image)

            # Extracting text line-by-line
            lines = []
            for page in result.pages:
                for block in page.blocks:
                    for line in block.lines:
                        line_text = " ".join([word.value for word in line.words])
                        lines.append(line_text)

            extracted_text = "\n".join(lines)

            # Very basic medicine name extraction
            meds = extracted_text.lower().split()
            conflicts = check_conflicts(meds)

        except Exception as e:
            extracted_text = f"❌ Failed to analyze prescription: {str(e)}"

    return render(request, "prescription_analyzer/analyze_prescription.html", {
        "text": extracted_text,
        "conflicts": conflicts
    })
