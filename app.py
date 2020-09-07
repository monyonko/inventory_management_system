
from flask import Flask,render_template,request,redirect,url_for,flash

import pygal
import psycopg2

from flask_sqlalchemy import SQLAlchemy

from Config.Config import Development,Production
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user



app = Flask(__name__)


# load configuration
app.config.from_object(Development)
# database://user:password@host:port/databasename

# calling/instanciating of Sqlalchemy
# comes with helpers and functions
db = SQLAlchemy(app)

bcrypt= Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view= 'login'
login_manager.login_message_category = 'info'

conn = psycopg2.connect("dbname='inventory_management_system' user= 'postgres' host='localhost' port='5432' password='borauhai' ")
cur = conn.cursor()

# creating tables
from models.inventory import InventoryModel
from stock import StockModel
from sales import SalesModel
from admin import Administration
from employee import Employee
from customer import User

# decorators
@app.before_first_request
def create_tables():
    db.create_all()



# creating of endpoints/route
# 1. declaration of a route 
@app.route('/')
 # 2.a function embedded to the route
def hello_world():
     return render_template('index.html')
   

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/service')
def service():
    return render_template('service.html') 

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html') 

@app.route('/view_sales/<inv_id>')
def view_sales(inv_id):
    cur.execute(f"""

    SELECT inv_id, sum(quantity) as "remaining_stock"
		FROM (SELECT st.inv_id, sum(quantity) as "quantity"
		FROM public.new_stock as st
		GROUP BY inv_id

			union all

			SELECT sa.inv_id, - sum(quantity) as "quantity"
		FROM public.new_sales as sa
		GROUP BY inv_id) as stsa
		WHERE inv_id={inv_id}
		GROUP BY inv_id;

    """)

    rec = cur.fetchall()
    print(rec)

    sales = SalesModel.get_sales_by_id(inv_id)
    inv_name = InventoryModel.fetch_by_id(inv_id)

    return render_template('view_sales.html', sales=sales, 
                            inv_name=inv_name)


@app.route('/inventories', methods=['GET', 'POST'])
def info():
    inventories=InventoryModel.query.all()

    # print(inventories)
    cur.execute("""   
SELECT inv_id, sum(quantity) as "remaining_stock" 		
FROM (SELECT st.inv_id, sum(quantity) as "quantity" 		
FROM public.new_stock as st 		
GROUP BY inv_id 
	  
	  union all 
	  
SELECT sa.inv_id, - sum(quantity) as "quantity" 	
FROM public.new_sales as sa 		
GROUP BY inv_id) as stsa 		
GROUP BY inv_id 		

ORDER BY inv_id;
        """ )

    remaining_stock=cur.fetchall()



    if request.method =='POST':
        name=request.form['name']
        inv_type=request.form['type']
        buying_price=request.form['buying_price']
        selling_price=request.form['selling_price'] 
 
        # print(name)
        # print(inv_type)
        # print(buying_price)
        # print(selling_price)

        '''
        STEPS TO INSERT RECORDS
        1.create yyour model object
        '''
        # insert records 
        new_inv = InventoryModel(name=name,inv_type=inv_type, buying_price=buying_price,selling_price=selling_price)
        new_inv.add_inventories()

        flash(f"Inventory added succesfully", "success")
        # InventoryModel.add_inventories(new_inv)
        return redirect (url_for('info')) 

    return render_template('info.html', inventories=inventories,remaining_stock=remaining_stock)

@app.route('/add_stock/<inv_id>', methods=['POST'])
def add_stock(inv_id):
    # print(inv_id)

    if request.method == 'POST':
        stock = request.form['stock']
        new_stock = StockModel(inv_id=inv_id, quantity=stock)
        new_stock.add_stock()

        return redirect (url_for('info'))  



@app.route('/make_sale/<inv_id>', methods=['POST'])
def make_sale(inv_id): 
    print(inv_id)
    if request.method =='POST':
    
        sale= request.form['quantity']
        new_sale = SalesModel(inv_id=inv_id, quantity=sale)
        new_sale.add_sale()
        # sale = request.form['sale']
        # print(sale)

        return redirect(url_for('info'))



@app.route('/edit_inventory/<inv_id>',methods=['GET', 'POST'])
def edit(inv_id):

    record=InventoryModel.query.filter_by(id=inv_id).first()

    if request.method == 'POST':

        name = request.form['name']
        inv_type = request.form['type']
        buying_price = request.form['buying_price']
        selling_price = request.form['selling_price']


        if record:
            record.name = name
            record.inv_type = inv_type
            record.buying_price= buying_price
            record.selling_price= selling_price

            db.session.commit()

        return redirect(url_for('info'))



@app.route('/data_visualization')
def data_visualization():
    
    cur.execute(""" 
    SELECT inv_type,count(inv_type)
	FROM public.new_inventories
	
	GROUP BY inv_type
    
    """)
    product_service = cur.fetchall()

    print(product_service)



    # initializing your pie chart
    
    pie_chart= pygal.Pie()
    '''

    my_pie_data = [
        ('Nairobi',40),
        ('Kilifi' ,10),
        ('Machakos' ,10),
        ('Kiambu' ,20),
        ('Nakuru',20)
        ]

'''
         
    pie_chart.title ='FRUITS AND VEGETABLES'
    for each in product_service:
        pie_chart.add(each[0],each[1])

    pie_data = pie_chart.render_data_uri()

    '''
    add components to your pie chart
        1.add title
        2.partition your pie chart

    
    pie_chart.add('Nairobi',40)
    pie_chart.add('Kilifi',10)
    pie_chart.add('Machakos',10)
    pie_chart.add('Kiambu',20)
    pie_chart.add('Nakuru',20)

'''
    # end of piechart

    # start of line_chart
    cur.execute("""
   SELECT EXTRACT(MONTH FROM s.created_at)as sales_month,sum (quantity  * selling_price) as total_sales
	FROM new_sales as s
	join new_inventories as i on s.inv_id=i.id
	group by sales_month
	order by sales_month asc;
    

    """)

    monthly_sales=cur.fetchall()
    # print(monthly_sales)

    a=[]
    b=[]
    for each in  monthly_sales :
        #  print(monthly_sales)
          
        x=each[0]
        y=each[1]

        a.append(x)
        b.append(y)

        line_chart = pygal.Line()
        line_chart.title = 'MONTHLY SALES'
        line_chart.x_label = a
        line_chart.add('Monthly Sales',b)

        
        line_data = line_chart.render_data_uri()


    return render_template('charts.html',chart=pie_data,line=line_data)
      
         
'''
    line_chart.add('Firefox',[None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome', [.3, .9, 17.1, 15.3, .6, .5, 1.6])
    line_chart.add('IE', [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others',[14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
'''


@app.route('/delete/<inv_id>')  
def delete_inventory(inv_id):
    
    record=InventoryModel.query.filter_by(id=inv_id).first()
    
    if record:
        db.session.delete(record)
        db.session.commit()
        flash("Inventory has been deleted", "success")
    else:
        print('Record does not exist')
    
    return redirect(url_for('info'))   

from forms import RegistrationForm, RegistrationForm1, RegistrationForm2, LoginForm



@login_manager.user_loader
def load_user(user_id):
    return Administration.query.get(int(user_id))

@app.route("/register", methods=['GET', 'POST'])
def register():
    
    form = RegistrationForm1()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Administration(f_name=form.f_name.data, l_name=form.l_name.data, username=form.username.data, email=form.email.data, 
            department= form.department.data, date_employed=form.date_employed.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your data has been added to the database', 'success')
        return redirect(url_for('c_register'))
    return render_template('register.html', title='Register', form=form)

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

@app.route("/e_register", methods=['GET', 'POST'])
def e_register():
    
    
    form = RegistrationForm2()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Employee(f_name=form.f_name.data, l_name=form.l_name.data, username=form.usernmae.data, email=form.email.data, 
             department=form.department.data, education_level=form.education_level.data, managed_by=form.managed_by.data, 
             salary= form.salary.data,
            date_employed=form.date_employed.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your data has been added succesfully', 'success')
        return redirect(url_for('c_register'))
    return render_template('register1.html', title='Register', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/c_register", methods=['GET', 'POST'])
def c_register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(f_name=form.f_name.data, l_name=form.l_name.data, username=form.usernmae.data, email=form.email.data, 
             password=hashed_password) 
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created. You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register2.html', title='Register', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
      return redirect(url_for('home'))
    form= LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccesful! Please check your username and password', 'danger')
    return render_template('log_in.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
    
#@app.route("/account")
#@login_required
#def account():
#    return render_template('account.html', title='Account')





#  run_your_app
if __name__=="__main__":
    app.run()