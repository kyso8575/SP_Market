from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, ProductImage

# Create your views here.

@login_required(login_url='accounts:login')  # 로그인하지 않은 경우 로그인 페이지로 리디렉션
def product_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        condition = request.POST.get("condition")
        images = request.FILES.getlist("images")  # 여러 이미지 받기

        # 필수 필드 검증
        if not all([name, description, price, condition]):
            return render(request, "products/product_create.html", {
                "error": "All fields are required"
            })

        # Product 객체 생성 및 저장
        product = Product.objects.create(
            seller=request.user,
            name=name,
            description=description,
            price=price,
            condition=condition
        )

        # 여러 이미지 저장
        for image in images:
            ProductImage.objects.create(product=product, image=image)

        return redirect('accounts:profile')  # 상품 목록 페이지로 리디렉션

    return render(request, "products/product_create.html")