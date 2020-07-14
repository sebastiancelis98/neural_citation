import psycopg2
import psycopg2.extras
from gensim.parsing import preprocessing
import contractions

def clean_text(text):
    """ Cleans the text in the only argument in various steps 
    ARGUMENTS: text: content/title, string
    RETURNS: cleaned text, string"""
    # Replace newlines by space. We want only one doc vector.
    text = text.replace('\n', ' ').lower()
    # Remove URLs
    #text = re.sub(r"http\S+", "", text)
    # Expand contractions: you're to you are and so on.
    text = contractions.fix(text)
    # Remove punctuation -- all special characters
    text = preprocessing.strip_multiple_whitespaces(preprocessing.strip_punctuation(text))
    return text

# Connect to Postgres
conn = psycopg2.connect("dbname=MAG19 user=mag password=1maG$ host=localhost port=8888")
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

file = open('input/mag_citing_data.txt', 'a')

query = """SELECT paperauthors.paperid, paperauthors.publishedyear, paperauthors.papertitle, paperauthors.referenceid, paperauthors.context, string_agg(authors.displayname::character varying, ',') AS citingauthors FROM
    (SELECT citingpaper.paperid, citingpaper.publishedyear, citingpaper.papertitle, citingpaper.referenceid, citingpaper.context, paperauthoraffiliations.authorid FROM
        (SELECT englishcspapers.paperid, englishcspapers.publishedyear, englishcspapers.papertitle, citationcontexts.referenceid, citationcontexts.context FROM
            (
                SELECT computersciencepapers.paperid, computersciencepapers.publishedyear, papertitle  FROM 
                (
                    SELECT papers.paperid, papers.publishedyear, papertitle  FROM papers 
                     INNER JOIN 
                    (SELECT paperid from paperfieldsofstudy WHERE fieldofstudyid=41008148) AS fieldsofstudy 
                     ON papers.paperid=fieldsofstudy.paperid
                ) AS computersciencepapers
                INNER JOIN 
                (SELECT paperid FROM paperlanguages WHERE languagecode='en') AS languages 
                ON languages.paperid=computersciencepapers.paperid
            ) AS englishcspapers INNER JOIN 
            (SELECT paperid, paperreferenceid AS referenceid, citationcontext AS context
            FROM papercitationcontexts) AS citationcontexts 
            ON citationcontexts.paperid=englishcspapers.paperid        
        ) AS citingpaper INNER JOIN
        (SELECT paperid, authorid FROM paperauthoraffiliations) AS paperauthoraffiliations
        ON paperauthoraffiliations.paperid=citingpaper.paperid
    ) AS paperauthors INNER JOIN
    (SELECT authorid, displayname FROM authors) AS authors
    ON authors.authorid=paperauthors.authorid
    GROUP BY paperauthors.paperid, paperauthors.publishedyear, paperauthors.papertitle, paperauthors.referenceid, paperauthors.context
    ORDER BY paperauthors.paperid"""
outputquery = 'copy ({0}) to stdout with csv header'.format(query)

with open('input/mag_citing_all.txt', 'w') as f:
    cur.copy_expert(outputquery, f)

cur.close()
conn.close()







    
