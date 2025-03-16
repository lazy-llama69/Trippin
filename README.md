<p align="center">
	<h2 align="center">Trippin</h2>
	<h4 align="center"> AI Travel Planner Web App
This web app offers a simple way to create and enhance personalized travel itineraries, allowing users to enjoy stress-free travel with easy itinerary building, expert recommendations, and a chatbot to assist with any questions.
<h4>
</p>



## Functionalities
<ol>
  <li><strong>Personalized Itinerary Creation:</strong><br> Users can input their travel preferences, including destination, budget, activities, and duration, to automatically generate a customized itinerary tailored to their needs.</li>
  
  <li><strong>Interactive Chatbot:</strong><br> A chatbot is available to assist users with real-time travel-related queries. It can offer activity suggestions, provide itinerary adjustments, and answer questions, creating a more interactive and responsive travel planning experience.</li>
  
  <li><strong>Activity & Destination Suggestions:</strong><br> Recommendations for local attractions, unique experiences, and hidden gems are provided to help travelers discover places and activities that match their interests.</li>
  
  <li><strong>Download and Export Itinerary:</strong><br> The finalized itinerary can be downloaded as a PDF or viewed on the web, allowing for offline viewing and sharing.</li>
  
  <li><strong>Currency Conversions:</strong><br> Users can convert currency based on their travel destination, providing real-time exchange rate information.</li>
  
  <li><strong>Itinerary Enhancement:</strong><br> Users can paste an existing itinerary into the platform, which will be refined and enhanced with additional suggestions, adjustments, and recommendations to improve the overall travel experience.</li>
  
  <li><strong>Tourist Recommendations & Travel Places:</strong><br> Detailed recommendations for popular tourist spots, cultural landmarks, and off-the-beaten-path locations are offered.</li>
  
  <li><strong>Travel FAQs:</strong><br> A comprehensive FAQ section is available to address common travel-related questions, offering useful advice and tips to help users plan their trip more effectively.</li>
  
  <li><strong>Random Generation of Itinerary:</strong><br> For users who need inspiration or are undecided on their next destination, a randomly generated itinerary is available.</li>
  
  <li><strong>Map Locations to Show Destination:</strong><br> The platform provides a map of the selected destination with markers for suggested places to visit, ensuring that users can easily navigate their destination and discover places of interest nearby.</li>
</ol>
<br>


## Instructions to run locally
* Install all pre-requisites 
```bash
$ pip install -r requirements.txt
```
* If any errors pop up during installation, just pip install one by one.
* Make secrets folder
```bash
$ mkdir .streamlit 
```
* Create the secrets.toml file in the folder and add your api_keys like this
[openai]
api_key = "your_openai_api_key_here"

[google]
maps_api_key = "your_google_api_key_here"

[exchange]
api_key = "your_exchange_api_key_here"

[gemini]
api_key = "your_gemini_api_key_here"

* Executing the source file
```bash
$ streamlit run streamlit_app.py
```
<br>

## Try it out on our hosted website
https://trippin.streamlit.app

<br>

## Contributors

<table>
<tr align="center">


<td>

Chang Yi Qian

<p align="center">

</p>
<p align="center">
<a href = "https://github.com/yiqianee"><img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36"/></a>
<a href = "https://www.linkedin.com/in/yi-qian-chang-048420228/">
<img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/>
</a>
</p>
</td>


<td>

Tang Jia Shen
<p align="center">

</p>
<p align="center">
<a href = "https://github.com/lazy-llama69"><img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36"/></a>
<a href = "https://www.linkedin.com/in/jia-shen-tang-b1a564170/">
<img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/>
</a>
</p>
</td>


<td>

Kueh Tze Shuen 
<p align="center">

</p>
<p align="center">
<a href = "https://github.com/KuehTzeShuen"><img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36"/></a>
<a href = "https://www.linkedin.com/in/shuen-kueh-89157723b/">
<img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/>
</a>
</p>
</td>



<td>

John Elisa
<p align="center">
</p>
<p align="center">
<a href = "https://github.com/johnbobelisa">
<img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36"/></a>
<a href = "https://www.linkedin.com/in/john-elisa-aa5843206/">
<img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/>
</a>
</p>
</td>
</tr>
  </table>
  
<br>

## Acknowledgments

This project utilizes several third-party APIs to provide enhanced functionality and improve the user experience. The following APIs are acknowledged for their valuable contributions:

<ol>
  <li>
    <strong>Gemini API:</strong><br>
    The Gemini API powers the chatbot functionality and enhances the PDF itinerary feature. It enables interactive conversations with users, answering travel-related queries and providing real-time assistance. The Gemini API also helps enhance the personalized travel itineraries by refining and formatting them into professional PDF documents.<br>
  </li>
  
  <li>
    <strong>Exchange Rate API:</strong><br>
    The Exchange Rate API is used for real-time currency conversions, enabling users to easily manage and convert currencies based on live market data.<br>
  </li>
  
  <li>
    <strong>OpenAI API:</strong><br>
    OpenAI's GPT-3 model is used to customize and generate personalized travel itineraries based on user preferences. It processes the user inputs to create detailed, dynamic, and customized itineraries, ensuring a tailored travel experience.<br>
  </li>
</ol>

<br>

## Important Note

If you fork or clone this repository, **please ensure to replace the API keys with your own,**. 

**Responsible usage of these resources is highly encouraged.**

<br>

## License
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

<p align="center">
	Hope you love our app! SLAY~ </a>
</p>


