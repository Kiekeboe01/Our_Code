from flask import Flask, render_template
import Database_connection as DataBase

app = Flask(__name__, template_folder='../templates', static_folder='../static')


@app.route('/')
@app.route('/home')
def home():
    """
    Renders the about us page of the Flask application.
    """
    return render_template("home.html")


@app.route('/results')
def results():  # put application's code here
    """
    Renders the results page of the Flask application.

    Returns:
        dates - list - all the dates from the articles from the database.
        authors - list - all the authors from the articles from the database.
        links - list - all the links from the articles from the database.
        titles - list - all the titles from the articles from the database.
        pubmedID - list - all the pubmedID from the articles from the database.
        keywords - list - all the keywords from the articles from the database.
    """

    # Retrieve column values for various columns
    dates = DataBase.retrieve_column_values("dates")
    authors = DataBase.retrieve_column_values("authors")
    links = DataBase.retrieve_column_values("links")
    titles = DataBase.retrieve_column_values("title")
    pubmedid = DataBase.retrieve_column_values("pubmed_id")
    keywords = DataBase.retrieve_column_values("keyword")

    return render_template("results.html", dates=dates, authors=authors, links=links, titles=titles, pubmedID=pubmedid,
                           keywords=keywords)


@app.route('/manual')
def manual():
    """
    Renders the manual page of the Flask application.
    """
    return render_template("manual.html")


@app.route('/about_us')
def about_us():
    """
    Renders the about us page of the Flask application.
    """
    return render_template("about_us.html")


if __name__ == '__main__':
    app.run(debug=True)
