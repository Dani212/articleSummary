from flask import Blueprint, request, render_template, abort

from ..service.summarize_service import SummarizeService

sum_app = Blueprint("summary", __name__,
                    template_folder="pages", static_folder="staticFiles")


@sum_app.get("/")
def hello_world():
    return render_template('home.html')


@sum_app.post("/submit")
def submit():
    try:
        summaryService = SummarizeService()
        # Summarize article from web form
        [articleText, summary] = summaryService.summarize(request=request)
        return render_template('home.html', summary=summary, articleText=articleText)
    except Exception as e:

        print(e)
        abort(404)


# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('home.html'), 404
