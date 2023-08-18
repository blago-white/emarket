<h1 align="center">
  <a href="https://е-маркет.рф/">
    <img src="https://github.com/blago-white/emarket/blob/main/emarket/static/img/emarket.jpg?raw=true" width=30>
  </a>
  E-MARKET
</h1>

<h3 align="center">
  Emarket is online market for buying and selling mobile phones powered on django framework
</h3>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

![Python ver](https://img.shields.io/badge/python-3.11-blue)
![Django ver](https://img.shields.io/badge/django-4.2.1-darkgreen)
![Psycopg2 ver](https://img.shields.io/badge/psycopg2-2.9.6-yellow)
![Nginx ver](https://img.shields.io/badge/nginx-latest-green)
![docker_compose ver](https://img.shields.io/badge/docker_compose-3.11-lightblue)

![SSL](https://img.shields.io/badge/SSL_Let's_Encript-lightgreen)
![OAuth2.0](https://img.shields.io/badge/OAuth_2.0-lightblue)

<h4 align="center">
  With e-market you can order, sell mobile phones, add new product cards and manage them
</h4>

<h4>
  The product card has several meanings:
  <h4>user-changeable:
  <ul type="circle">
    <li>title</li>
    <li>category</li>
    <li>preview card</li>
    <li>price</li>
    <li>product color</li>
    <li>device storage size</li>
    <li>count of products</li>
  </ul>
  </h4>
  <h4>hidden:
  <ul type="circle">
    <li>card id</li>
    <li>views <sup>*the more views on your card, the higher it is in the list</sup></li>
    <li>owner</li>
  </ul>
  </h4>
</h4>

<h3>Steps to recreate the emarket and launch it on localhost</h3>
<ol>
  <li>Install <b>python 3.11.0</b> and <b>git</b></li>
  <li>Create <b>python venv</b> in directory <code>...\somedir\emarket</code> <code>python -m venv path\to\myenv</code></li>
  <li><b>Clone this repo</b> with command <code>git clone https://github.com/blago-white/emarket.git</code> from the <code>...\somedir</code></li>
  <li>
    <b>Сreate a file .env</b> in the root of the project and fill it with your data
    <pre>SECRET_KEY=`django secret key`
POSTGRES_HOST=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_TEST_PASSWORD=...
POSTGRES_DB=...
POSTGRES_PORT=...
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
DEFAULT_FROM_EMAIL=$EMAIL_HOST_USER</pre>
  </li>
  <li><b>Activate the venv</b> from <code>...\somedir\emarket</code> with command: <code>venv\Scripts\activate</code> on windows or <code>source venv/bin/activate</code> in linux</li>
  <li>Run <code>pip install -r requirements.txt</code> from <code>...\somedir\emarket</code> to <b>install dependencies</b></li>
  <li><b>Run migrations</b> with: 
    <ol type="1">
      <li><code>python emarket\manage.py makemigrations --setting=emarket.testsettings</code></li>
      <li><code>python emarket\manage.py migrate --setting=emarket.testsettings</code></li>
    </ol>
  </li>
  <li><b>Run the testserver</b> from <code>...\somedir\emarket</code> <code>python emarket\manage.py runserver --setting=emarket.testsettings --insecure</code></li>
  <li><b>✨Perfectly!Go to <a href="http://127.0.0.1:8000">localhost</a> and enjoy the site!</b></li>
</ol>

<h6 align="center">for all questions, write ✉ bogdanloginov31@gmail.com</h6>
