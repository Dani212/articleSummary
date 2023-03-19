from .extract_text import ExtractByFileType

import requests
import validators


class SummarizeService:
    def __get_summary(self, article):
        # Define the API endpoint and API key
        base_url = "https://api.smmry.com"
        API_KEY = "33DB752F19"
        response = None
        error = None
        params = {"SM_API_KEY": API_KEY}

        try:
            if validators.url(article):
                params["SM_URL"] = article
                # Make the API request
                response = requests.get(base_url, params=params)
            else:
                data = {"sm_api_input": article}

                header_params = {"Expect": "100-continue"}
                # Make the API request
                response = requests.post(
                    base_url, params=params, data=data, headers=header_params)
                # print(response.status_code)


            print(response.json())
            # Get the summary from the response
            summary = ""
            if "sm_api_error" in response.json():
                error= response.json()["sm_api_message"]
            else:
                summary = response.json()["sm_api_content"]

            return [summary, error]
        except requests.exceptions.HTTPError as e:
            return [summary, "An error occur try again later"]

    def summarize(self, request):
        article = request.form['article']
        try:
            if isinstance(article, str) and article.strip() != "":
                minimum_words = 1000
                number_of_words = len(article.split(' '))
                is_text_valid = number_of_words >= minimum_words

                if validators.url(article) and is_text_valid:
                    return [article, "", "Invalid text"]

                [summary, error] = self.__get_summary(article)
                return [article, summary, error]
            else:
                extract_by_file_type = ExtractByFileType()
                article = extract_by_file_type.extract_text_by_type(
                    request=request)

                # print(article)
                [summary, error] = self.__get_summary(article)
                return [article, summary, error]

        except requests.RequestException as e:
            return [article, "", "un expect error occur"]
