<h3> Install </h3>
<p>&bull; pip install -r requirements.txt</p>
<h3>
Run:</h3>
<p>&bull; python main.py "csv_path"</p>

<h4>
Initiation Flow:</h4>
<p>&bull; csv_path doesn't exist we use default.csv</p>
<p>&bull; path exists - we load it </p>

<p>
&bull; Preprocessing: when the db is first loaded we sort list and update success values 
</p>
<h3>Tests: </h3>
<p>From tests folder path run: pytest -q <test-file-name></test-file-name></p>

<h4>Docker</h4>
<p>&bull; Build: docker build -t flight-catcher . </p>
<p>&bull; Run: docker run -it -p 5000:5000 flight-catcher</p>
<p>No swagger yet</p>
<p>API REQUESTS:api_requests.json </p>