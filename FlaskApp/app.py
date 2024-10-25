from flask import Flask, render_template, request, redirect, url_for, flash, session
import statistics  # Для вычисления средней стоимости

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_COOKIE_NAME'] = 'login_session'

USERNAME = 'admin'
PASSWORD = 'password'

records = []
products = []  # Список продуктов

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash("Неверный логин или пароль", "error")
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Проверка на добавление продукта
        new_product = request.form.get('new_product')
        if new_product:
            products.append(new_product)

        # Сохранение записи
        title = request.form.get('title')
        inn = request.form.get('inn')
        product = request.form.get('product')
        date = request.form.get('date')
        cost = request.form.get('cost')

        if not title or not inn or not product or not date or not cost:
            flash("Все поля должны быть заполнены!", "error")
        else:
            records.append({'title': title, 'inn': inn, 'product': product, 'date': date, 'cost': float(cost)})
            return redirect(url_for('home'))

    total_sales = len(records)
    total_cost = sum(record['cost'] for record in records)
    average_cost = total_cost / total_sales if total_sales > 0 else 0

    return render_template('index.html', records=records, products=products, total_sales=total_sales, average_cost=average_cost, total_cost=total_cost)

@app.route('/3D_models')
def models():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('3D_models.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)