

import psycopg2
import psycopg2.extras
from gensim.parsing import preprocessing
import contractions

# Connect to Postgres
conn = psycopg2.connect("dbname=mag_20200619 user=citerecdemo password=2qPF7FV8TutgPfGXCZ host=aifb-ls3-maia.aifb.kit.edu port=5432")
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

query = """SELECT citedauthors.paperid, citedauthors.publishedyear, citedauthors.referenceid, citedauthors.context, citedauthors.papertitle, string_agg(authors.displayname::character varying, ',') AS groupedcitedauthors FROM
    (SELECT citedpapertitle.paperid, citedpapertitle.publishedyear, citedpapertitle.referenceid, citedpapertitle.context, citedpapertitle.papertitle, paperauthoraffiliations.authorid FROM    
        (SELECT citingpaper.paperid, citingpaper.publishedyear, citingpaper.referenceid, citingpaper.context, citedpaper.papertitle FROM        
            (SELECT englishcspapers.paperid, englishcspapers.publishedyear, citationcontexts.referenceid, citationcontexts.context FROM    
                (
                    SELECT computersciencepapers.paperid, computersciencepapers.publishedyear FROM 
                    (
                        SELECT papers.paperid, papers.publishedyear FROM papers 
                         INNER JOIN 
                        (SELECT paperid from paperfieldsofstudy WHERE fieldofstudyid=41008148) AS fieldsofstudy 
                         ON papers.paperid=fieldsofstudy.paperid
                    ) AS computersciencepapers
                    INNER JOIN 
                    (SELECT paperid FROM paperurls WHERE languagecode='en') AS languages 
                    ON languages.paperid=computersciencepapers.paperid
                ) AS englishcspapers INNER JOIN             
                (SELECT paperid, paperreferenceid AS referenceid, citationcontext AS context
                FROM papercitationcontexts) AS citationcontexts 
                ON citationcontexts.paperid=englishcspapers.paperid             
            ) AS citingpaper INNER JOIN
            (SELECT paperid, papers.papertitle FROM papers) AS citedpaper
            ON citedpaper.paperid=citingpaper.referenceid       
        ) AS citedpapertitle INNER JOIN
        (SELECT paperid, authorid FROM paperauthoraffiliations) AS paperauthoraffiliations
        ON paperauthoraffiliations.paperid=citedpapertitle.referenceid
    ) AS citedauthors INNER JOIN
    (SELECT authorid, displayname FROM authors) AS authors
    ON authors.authorid=citedauthors.authorid       
    GROUP BY citedauthors.paperid, citedauthors.publishedyear, citedauthors.referenceid, citedauthors.context, citedauthors.papertitle
    ORDER BY citedauthors.paperid"""
    
outputquery = 'copy ({0}) to stdout with csv header'.format(query)

with open('input/mag_cited_all.txt', 'w') as f:
    cur.copy_expert(outputquery, f)

cur.close()
conn.close()







    
