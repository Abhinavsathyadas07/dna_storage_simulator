# dna_storage_simulator/interface/web_dashboard/app.py

from flask import Flask, request, render_template_string
from modules.encoders import DNAEncoder
from modules.compressors import HuffmanCompressor
from modules.error_correction import HammingECC
from modules.error_models import SubstitutionErrorModel

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        text = request.form["text"]
        error_rate = float(request.form.get("error_rate", 0.01))
        compressor = HuffmanCompressor()
        encoder = DNAEncoder()
        ecc = HammingECC()
        errors = SubstitutionErrorModel(error_rate)
        codes, compressed = compressor.compress(text)
        dna = encoder.encode(compressed)
        ecc_bits = ecc.encode(compressed)
        corrupted_dna = errors.introduce_errors(dna)
        recovered, errors_corrected = ecc.decode(ecc_bits)
        decompressed = compressor.decompress(codes, recovered)
        result = {
            "original": text,
            "compressed": compressed,
            "dna": dna,
            "corrupted_dna": corrupted_dna,
            "errors_corrected": errors_corrected,
            "decompressed": decompressed,
        }
    return render_template_string("""
        <h1>DNA Storage Simulator</h1>
        <form method="post">
            <textarea name="text" rows="4" cols="50" required></textarea><br>
            Error rate: <input type="number" name="error_rate" step="0.01" value="0.01"><br>
            <input type="submit" value="Submit">
        </form>
        {% if result %}
            <h2>Results</h2>
            <pre>{{ result }}</pre>
        {% endif %}
    """, result=result)

if __name__ == "__main__":
    app.run(debug=True)
