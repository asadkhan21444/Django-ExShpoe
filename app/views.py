from django.shortcuts import render , redirect
from .models import Customer, Product, Category,Order
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from app.middleware.auth import auth_middleware
from django.utils.decorators import method_decorator



# ==========================================================

class home(View):
    @method_decorator(auth_middleware)
    def post(self, request):
        product = request.POST.get('product')  # HTML se aaya
        remove = request.POST.get('remove')    # Remove flag
        print("product_id:", product)

        # Get existing cart from session, default empty dict
        cart = request.session.get('cart', {})

        # Agar product pehle se cart mein hai
        if cart.get(product):
            quantity = cart[product]
            if remove:
                if quantity <= 1:
                    cart.pop(product)  # Agar quantity 1 ya less → remove completely
                else:
                    cart[product] = quantity - 1
            else:
                cart[product] = quantity + 1
        else:
            # Agar product pehle cart mein nahi hai
            cart[product] = 1

        # Save back to session
        request.session['cart'] = cart
        # print("Current cart:", cart)
        # Redirect with fragment to scroll to product
        return redirect(f"/#product-{product}")
       

        # return redirect('home')

    
    def get(self, request):
    # REMOVE: request.session.get('cart').clear()
        products = None
        categories = Category.objects.all()  # Database se categories lena

        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_category_id(categoryID)
        else:
            products = Product.get_all_products()

        # Ensure cart exists in session
        cart = request.session.get('cart')
        if cart is None:
            request.session['cart'] = {}

        context = {
            'products': products,
            'categories': categories,
            'cart': request.session['cart'],  # send cart to template
        }

        return render(request, 'app/home.html', context)

 
# ==========================================================

class signup(View):
    def get(self,request):
        return render(request,'app/signup.html')
    
    def post(self,request):
        postdata = request.POST
        first_name = postdata.get('first_name')
        last_name = postdata.get('last_name')
        phone = postdata.get('phone')
        email = postdata.get('email')
        password = postdata.get('password')

        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
        }

        #  customer pehle banao (IMPORTANT FIX)
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            password=password
        )

        #  ab validation sahi chalegi
        error_message = self.customervalidate(customer)

        # saving
        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('login')   #  HttpResponse

        else:
            context = {
                'error': error_message,
                'values': value
            }
            return render(request, 'app/signup.html', context)
        
        
    def customervalidate(self,customer):
        error_message = None
        if not customer.first_name:
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 4:
            error_message = "First Name must be 4 char long or more"
        elif not customer.phone:
            error_message = "Phone Number Required !!"
        elif len(customer.phone) < 10:
            error_message = "Phone Number must be 10 char long"
        elif len(customer.password) < 6:
            error_message = "Password must be 6 char long"
        elif Customer.objects.filter(email=customer.email).exists():
            error_message = "Email already registered"
            
        return error_message

# ==========================================================
class Orders(View):
    def get(self, request):
        customer_id = request.session.get('customer')
        if not customer_id:
            return redirect('login')

        orders = Order.objects.filter(customer_id=customer_id).order_by('-date')
        # print(orders)
        return render(request, 'app/order.html', {'orders': orders})



# ==========================================================
class login(View):
    def get(self, request):
        return render(request, 'app/login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        customer = Customer.objects.filter(email=email).first()

        if customer:
            if check_password(password, customer.password):
                request.session['customer'] = customer.id  # session set
                return redirect('home')
            else:
                error_message = "Invalid password"
        else:
            error_message = "Email not registered"
        
        context = {
            'error': error_message,
            'values': {'email': email}
        }
        return render(request, 'app/login.html', context)

# ==========================================================

def logout(request):
    if 'customer' in request.session:
        del request.session['customer']
    return redirect('login')


# ===============================================================

class Cart(View):
    def get(self, request):

        cart = request.session.get('cart')

        # Agar cart hi nahi
        if not cart:
            return render(request, 'app/cart.html', {'products': []})

        # sirf valid ids lo
        ids = [int(k) for k in cart.keys() if k.isdigit()]

        products = Product.get_products_by_id(ids)
        print("CART:", request.session.get('cart'))
        # print("IDS:", ids)

        return render(request, 'app/cart.html', {'products': products})
    
    
# ========================================================================
class Checkout(View):
    def post(self, request):

        customer_id = request.session.get('customer')
        cart = request.session.get('cart')

        if not customer_id or not cart:
            return redirect('cart')

        #  IMPORTANT FIX
        ids = [int(k) for k in cart.keys() if k.isdigit()]
        products = Product.get_products_by_id(ids)

        customer = Customer.objects.get(id=customer_id)

        for product in products:
            Order.objects.create(
                customer=customer,
                product=product,
                price=product.price,
                quantity=cart.get(str(product.id))
            )

        request.session['cart'] = {}
        return redirect('order')
# ==========================================================
# ==========================================================


    
  