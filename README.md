<section style="max-width:700px; margin:auto; font-family:Arial, sans-serif; line-height:1.7; color:#333;">
  <h1 style="text-align:center; color:#2c3e50;">Django Shop Website</h1>

  <p align="center">
  <img src="./docs/shop.png" width="700"/>
  </p>

  <h2 style="color:#34495e;">About the Project</h2>
  <p>
     This is a Django e-commerce website with features such as product management, shopping cart, coupons, orders, ratings, comments, and payment integration.
  </p>

  <h2 style="color:#34495e;">Project Goal</h2>
  <p>
    I developed this project to improve my understanding of database relationships in e-commerce systems, shopping cart implementation, order management, and other related concepts.
  </p>
</section>

<h2>Features</h2>
<ul>
  <li>Session Authentication</li>
  <li>Iranian Phone Number Validation</li>
  <li>Role-Based Permissions</li>
  <li>Admin & Customer Dashboards</li>
  <li>Product Filtering</li>
  <li>Product Ordering</li>
  <li>Product Searching</li>
  <li>Product Rating</li>
  <li>Product Commenting</li>
  <li>Shopping Cart</li>
  <li>Coupon System</li>
  <li>Order Management</li>
  <li>Payment Integration</li>
</ul>


<h2>Technologies</h2>
<ul>
  <li> Python</li>
  <li> Django</li>
  <li> SQLite</li>
  <li> Django Signals</li>
  <li> HTML, CSS, JavaScript</li>
</ul>

<h2>⚙️ Installation (Windows)</h2>

<p>Follow these steps to set up and run the project locally.</p>

<hr>

<h3>1. Clone the repository</h3>

```bash
git clone https://github.com/mhmdheydarii/Django-Shop-Website.git
```

<br>

<h3>2. Navigate to the project directory</h3>

```bash
cd Django-Shop-Website
```

<br>

<h3>3. Create a virtual environment</h3>

```bash
python -m venv .venv
```

<br>

<h3>4. Activate the virtual environment</h3>

<p><b>CMD</b></p>

```cmd
.venv\Scripts\activate
```

<p><b>PowerShell</b></p>

```powershell
.\.venv\Scripts\Activate.ps1
```

<p>
After activation, you should see something similar to:
</p>

```bash
(.venv)
```

<p>
at the beginning of your terminal line.
</p>

<br>

<h3>5. Install dependencies</h3>

<p>If the project includes a <code>requirements.txt</code> file:</p>

```bash
pip install -r requirements.txt
```

<h3>6. Configure environment variables</h3>

<p>Create a .env file in the project root and add the required environment variables.</p>

```bash
SECRET_KEY = your_secret_key
DEBUG = True
ALLOWED_HOSTS = "*"
TIME_ZONE = "UTC"
```
<br>

<h3>7. Run the project</h3>


```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
```bash
python manage.py runserver
```

<hr>

<details>
<summary><b>❌ Deactivate Virtual Environment</b></summary>

<br>

To exit the virtual environment:

```bash
deactivate
```

</details>

<br>

<p align="center">
⭐ If you found this project useful, consider giving it a star.
</p>
