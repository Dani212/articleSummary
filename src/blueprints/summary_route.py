from flask import Blueprint, request, render_template, abort

from ..service.summarize_service import SummarizeService

sum_app = Blueprint("summary", __name__,
                    template_folder="pages", static_folder="staticFiles")


@sum_app.get("/")
def hello_world():
    return render_template('index.html')

@sum_app.route("/summarize", methods=["GET", "POST"])
def summarize():
    if request.method == "GET":
        return render_template("home.html")
    else:        
        errors = []
        summaryService = SummarizeService()
        # Summarize article from web form
        [articleText, summary, error] = summaryService.summarize(request=request)
        if error is not None:
            errors.append(error)
        return render_template("home.html", 
                               summary=summary, articleText=articleText, errors=errors)
 
# # @app.errorhandler(404)
# # def page_not_found(error):
# #     return render_template('home.html'), 404
