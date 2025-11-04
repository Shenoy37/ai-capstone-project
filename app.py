import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from werkzeug.middleware.proxy_fix import ProxyFix

from app.brd_generator import BRDGenerator
from app.docx_exporter import build_brd_document


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-secret")
    app.wsgi_app = ProxyFix(app.wsgi_app)

    generator = BRDGenerator()

    @app.route("/", methods=["GET", "POST"])
    def index():
        generated_brd = None
        input_text = ""
        selected_domain = "pharma"
        additional_notes = ""
        if request.method == "POST":
            input_text = request.form.get("project_description", "").strip()
            selected_domain = request.form.get("domain", "pharma")
            additional_notes = request.form.get("additional_notes", "").strip()

            if not input_text:
                flash("Please provide project context before generating a BRD.", "error")
                return render_template(
                    "index.html",
                    brd=generated_brd,
                    input_text=input_text,
                    selected_domain=selected_domain,
                    additional_notes=additional_notes,
                )

            generated_brd = generator.generate_brd(
                domain=selected_domain,
                project_description=input_text,
                additional_notes=additional_notes,
            )
            session["generated_brd"] = generated_brd
            session["project_description"] = input_text
            session["selected_domain"] = selected_domain
            session["additional_notes"] = additional_notes

        else:
            session.pop("generated_brd", None)
            session.pop("project_description", None)
            session.pop("selected_domain", None)
            session.pop("additional_notes", None)

        return render_template(
            "index.html",
            brd=generated_brd,
            input_text=input_text,
            selected_domain=selected_domain,
            additional_notes=additional_notes,
        )

    @app.route("/download", methods=["GET"])
    def download():
        brd = session.get("generated_brd")
        if not brd:
            flash("No BRD available to download. Generate one first.", "error")
            return redirect(url_for("index"))

        document = build_brd_document(brd)
        output_filename = f"{brd.get('title', 'business-requirements')}.docx"
        output_filename = output_filename.replace(" ", "-").lower()

        return send_file(
            document,
            as_attachment=True,
            download_name=output_filename,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
