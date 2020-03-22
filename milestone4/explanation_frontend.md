## Frontend explanation

The HTML/javascript front-end comprises of 3 html documents, 1 javascript document and 1 CSS stylesheet.

#### Technical details of each frontend file:

- `frontend.html`: this is the frontpage for visitors when they load up the local web server. It contains a heading; a description of our annotated tweet corpus; a left sidebar containing form elements for keyword search, filtering options(3 languages, 4 companies, and 5 sentiment scales) and links to visualizations; and a big space on the right to return query results.  A table/chart page will show up on the right in response to visitor's selection of the checkboxes on the left sidebar. 
 
- `frontend_barcharts.html`: this is the page containing 3 static bar charts of average sentiment towards the 4 tech companies across English, French and Chinese. It provides a brief conclusion of the data in the annotated corpus.
 
- `frontend_piecharts.html`: this is the page containing 20 static piecharts of sentiment rating breakdown that are organized into 4 subpages, each corresponding to one single company. The buttons on top will hide some charts from sight. To provide interactability, when visitors click on button of individual companies, more refined breakdown sentiment distribution charts across different language speakers will load into sight.   

- `frontend.js`: this javascript file comprises of functions that respond to actions visitors perform on the left sidebar of frontend.html. Submit_form() will pass the query entered in the frontend to the python backend, return the query results from the annotation corpus and update a portion of frontend.html. openTab() will hide subpages inside frontend_piecharts.html when it opens up, to make the page cleaner and more organized.

- `frontend.css`: this stylesheet carries the visual asthetics of html pages, including the color scheme for background, fonts and tables. The dynamic use of CSS also allows some interactive animation effects(change in background color, font color, shift of position and padding etc) when a visitor hover their mouse over certain elements on the webpage. 

