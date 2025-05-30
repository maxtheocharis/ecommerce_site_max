from django.shortcuts      import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models               import Product, Cart, CartItem, Order, OrderItem
from django.shortcuts      import render, redirect
from django.contrib.auth   import login
from .forms                import SignUpForm


@login_required
def update_cart_item(request, item_id):
    """Handle quantity changes or removal of a cart item."""
    ci = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == 'POST':
        # If they clicked “Remove”, delete it
        if 'remove' in request.POST:
            ci.delete()
        else:
            # Otherwise update quantity
            qty = int(request.POST.get('quantity', ci.quantity))
            if qty > 0:
                ci.quantity = qty
                ci.save()
            else:
                ci.delete()

    return redirect('view_cart')







@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()

    # Build a list of line‐items with subtotal
    items = []
    total = 0
    for ci in cart_items:
        price    = ci.product.price
        quantity = ci.quantity
        subtotal = price * quantity
        items.append({
            'product':  ci.product,
            'quantity': quantity,
            'price':    price,
            'subtotal': subtotal,
        })
        total += subtotal

    if request.method == 'POST':
        # create the Order
        order = Order.objects.create(
            user=request.user,
            total_price=total,
            status='pending'
        )
        # create the OrderItems
        for line in items:
            OrderItem.objects.create(
                order=order,
                product=line['product'],
                quantity=line['quantity'],
                price=line['price'],
            )
        # clear the cart
        cart.items.all().delete()
        return redirect('thank_you')

    return render(request, 'catalog/checkout.html', {
        'items': items,
        'total': total,
    })


@login_required
def thank_you(request):
    return render(request, 'catalog/thank_you.html')






def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = SignUpForm()
    return render(request, 'catalog/signup.html', {'form': form})



def product_list(request):
    products = Product.objects.all()
    return render(request, 'catalog/index.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/index1.html', {'product': product})

@login_required
def add_to_cart(request, pk):
    product, _ = get_object_or_404(Product, pk=pk), None
    cart, _    = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'catalog/cart.html', {'cart': cart})


@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    # Build a list of items with computed subtotals
    items = []
    total = 0
    for ci in cart.items.select_related('product'):
        subtotal = ci.product.price * ci.quantity
        items.append({
            'product': ci.product,
            'quantity': ci.quantity,
            'price':    ci.product.price,
            'subtotal': subtotal,
        })
        total += subtotal

    return render(request, 'catalog/cart.html', {
        'items': items,
        'total': total,
    })


@login_required
def view_cart(request):
    # 1) Get or create the user's cart
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # 2) Build a list of items with computed subtotals
    items = []
    total = 0
    for ci in cart.items.select_related('product'):
        subtotal = ci.product.price * ci.quantity
        items.append({
            'id':       ci.id,
            'product':  ci.product,
            'quantity': ci.quantity,
            'price':    ci.product.price,
            'subtotal': subtotal,
        })
        total += subtotal

    # 3) Render the cart template with our items and total
    return render(request, 'catalog/cart.html', {
        'items': items,
        'total': total,
    })