import flask
import rdflib
from flask import request
from flask import render_template, redirect, url_for
import wikipedia
from forms import SearchForm, SearchForm2
from flask_wtf.csrf import CSRFProtect, CSRFError

import os
SECRET_KEY = b'\x9aN\xa0\xedp\xff\x07 \xa4$\xbdn\x02\x1f\xce\x1c\xca,wBX\xd6F\xf3\x08?,/\xaf"\x0f5'


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = "data"
app.config["DEBUG"] = True

csrf = CSRFProtect(app)

g = rdflib.Graph()


g.parse("data/music_ontology.owl")


@app.route('/api/albums', methods=['GET'])
def albums():
    code = 200
    try :
        qres = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX owl: <http://www.w3.org/2002/07/owl#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        PREFIX ex: <http://www.semanticweb.org/macbook/ontologies/2021/11/Music#>
                        SELECT ?subject 
                        WHERE { ?subject rdf:type ex:Album }""")

        if len(list(qres))==0:
            code = 200
            res = []
        else :
            res = [x[0].n3().split("#")[1].split('>')[0] for x in list(qres)]
    except :
        code = 503
    return {"code":code,"response":res}



@app.route('/api/clients', methods=['GET'])
def clients():
    code = 200
    try :
        qres = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX owl: <http://www.w3.org/2002/07/owl#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        PREFIX ex: <http://www.semanticweb.org/macbook/ontologies/2021/11/Music#>
                        SELECT ?subject 
                        WHERE { ?subject rdf:type ex:Client }""")

        if len(list(qres))==0:
            code = 200
            res = []
        else :
            res = [x[0].n3().split("#")[1].split('>')[0] for x in list(qres)]
    except :
        code = 503

    return {"code":code,"response":res}


def get_artist_name(individu):
    code = 200
    if individu == '':
        code = 404
        res = None
    else :
        try :
            qres2 = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                                                PREFIX xd: <http://www.semanticweb.org/macbook/ontologies/2021/11/Music#>

                                                SELECT ?object 
                                                    WHERE { ?object xd:vendre xd:""" + individu + """  .                   
                                                    }""")

            res = [x[0].n3().split("#")[1].split('>')[0] for x in list(qres2)]
        except :
            code = 503
            res = None


    return {"code":code,"response":res}



def get_Artiste(artiste):

    code = 200
    if artiste == '':
        code = 404
        res = None
    else :
        try :
            qres2 = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                                                PREFIX xd: <http://www.semanticweb.org/macbook/ontologies/2021/11/Music#>

                                                SELECT  ?subject 
                                                WHERE { xd:""" + artiste + """ rdf:type ?subject}""")


            role = [x[0].n3().split("#")[1].split('>')[0] for x in list(qres2)]
        except :
            code = 503
            res = None

        qres3 = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                                        PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                                                        PREFIX xd: <http://www.semanticweb.org/macbook/ontologies/2021/11/Music#>

                                                        SELECT  ?chanson 
                                                        WHERE {
                                                        xd:""" + artiste + """  xd:composer ?chanson.}""")

        chanson = [x[0].n3().split("#")[1].split('>')[0] for x in list(qres3)]

        qres4 = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                                        PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                                                        PREFIX xd: <http://www.semanticweb.org/macbook/ontologies/2021/11/Music#>

                                                        SELECT  ?album
                                                        WHERE { xd:""" + artiste + """  xd:vendre ?album. }""")

        album = [x[0].n3().split("#")[1].split('>')[0] for x in list(qres4)]

    return {"code":code,"role":role, "chanson":chanson, "album":album}



def album_details(individu):

    code = 200
    if individu == '':
        code = 404

    else :
        try :
            qres2 = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                                                PREFIX xd: <http://www.semanticweb.org/macbook/ontologies/2021/11/Music#>

                                                SELECT ?prix ?ventes ?rating ?date_sortie
                                                    WHERE { xd:""" + individu + """ xd:prix ?prix.
                                                            xd:""" + individu + """ xd:ventes ?ventes.   
                                                            xd:""" + individu + """ xd:rating ?rating. 
                                                            xd:""" + individu + """ xd:date_sortie ?date_sortie.          
                                                    }""")


            prix= str(list(qres2)[0][0])
            ventes = str(list(qres2)[0][1])
            rating= str(list(qres2)[0][2])
            date_sortie= str(list(qres2)[0][3])
        except :
            code = 503


    return {"code":code, "prix":prix, "ventes":ventes, "rating":rating, "date_sortie":rating}


def individu_clients(individu):

    code = 200
    if individu == '':
        code = 404
        res = None
    else :
        try :
            qres = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            PREFIX owl: <http://www.w3.org/2002/07/owl#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                            PREFIX xd: <http://www.semanticweb.org/macbook/ontologies/2021/11/Music#>

                            SELECT ?object 
                                WHERE { xd:""" + individu + """ xd:acheter ?object.                   
                                }""")

            res = [x[0].n3().split("#")[1].split('>')[0] for x in list(qres)]
        except :
            code = 503
            res = None

        qres2 = g.query("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                                    PREFIX xd: <http://www.semanticweb.org/macbook/ontologies/2021/11/Music#>

                                    SELECT ?object 
                                        WHERE { ?object xd:vendre xd:""" + str(res)[2:-2] + """  .                   
                                        }""")

        res2 = [x[0].n3().split("#")[1].split('>')[0] for x in list(qres2)]

    return {"code":code,"response":(str(res)[2:-2].replace("_", " "), str(res2)[2:-2].replace("_", " "))}


def get_wikipedia_info(location):
    source = None
    if location == '':
        code = 404
        response = None
    else :
        code = 200
        try :
            response = wikipedia.summary(location)
            source = "wikipedia"
        except :
            code = 503
            response = None
    return {"code":code,"response":response,"source":source}


def get_info(location):
    data = None
    if location == '':
        code = 404
        artiste = None
    else :
        code = 200
        try :
            artiste = get_artist_name(location)
            data = album_details(location)
            #response = wikipedia.summary(location)
            #source = "wikipedia"
        except :
            code = 503
            data = None


    return {"code":code,"artiste":artiste, "data":data}


@app.route('/', methods = ['GET', 'POST'])
def home_page():
    form2 = SearchForm2()
    if request.method == 'POST' and form2.validate_on_submit():
        return redirect((url_for('search_data', query=form2.search2.data)))

    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        return redirect((url_for('search_results', query=form.search.data)))



    output = albums()
    individus=clients()
    if output['code'] == 200:
        return render_template('index.html' , albums = output["response"],individus = individus["response"],form1=form, form2=form2)
    elif output['code'] == 404:
        return render_template('404.html')
    else:
        return render_template('503.html')

@app.route('/album/<title>', methods = ['GET'])
def template_album(title):
    output = get_artist_name(title)
    album_data = album_details(title)
    if output['code'] == 200 :
        artiste = output['response']
    else :
        artiste = str(0)
    print(album_data)
    if album_data['code'] == 200 :
        prix = album_data['prix']
        ventes = album_data['ventes']
        date_sortie = album_data['date_sortie']
        rating = album_data['rating']
    else :
        response = []
    return render_template('template_album.html', prix=prix, ventes=ventes, date_sortie=date_sortie, rating=rating ,artiste = artiste , title = title)


@app.route('/individus/<individu>', methods = ['GET'])
def template_individu(individu):
    output = individu_clients(individu)

    if output['code'] == 200 :
        Album_data = output['response']
    else :
        Album_data = []
    return render_template('template_individus.html' ,Album_data = Album_data , individu = individu)


@app.route('/search_results/<query>')
def search_results(query):
  output = get_wikipedia_info(query)
  source = output['source']
  content = output['response']
  return render_template('search_results.html', query=query, content=content,source=source)

@app.route('/search_data/<query>')

def search_data(query):
    if (query in ['Album_5', 'equal','love_on_the_beat','studio_doo_wops_hoolingans' ]):
        output = get_info(query)
        artiste = output['artiste']
        data = output['data']
        if (data != None):
            prix=data["prix"]
            rating=data["rating"]
            ventes=data["ventes"]
            date_sortie=data["date_sortie"]
        else:
            prix = None
            rating = None
            ventes = None
            date_sortie = None
        return render_template('search_data.html', query=query, artiste=artiste,data=data, prix=prix,
                               ventes=ventes, rating=rating, date_sortie=date_sortie)

    elif (query in ['alex_beaupain', 'Bruno_Mars', 'Ed_Sheeran', 'Maroon_5']):
        output = get_Artiste(query)
        if (output != None):
            role = str(output["role"][1:])[2:-2].replace("'"," ")
            chanson = str(output["chanson"])[2:-2].replace("_"," ")
            album = str(output["album"])[2:-2].replace("_"," ")

        else:
            role = None
            chanson = None
            album = None


        return render_template('search_data_artiste.html', query=query,  output=output, role=role, chanson=chanson, album=album)

    else :

        return render_template('503.html')



if __name__ == "__main__":
    app.run()
