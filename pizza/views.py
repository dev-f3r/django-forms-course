from django.shortcuts import render
from .forms import PizzaForm


def home(request):
    return render(request, "pizza/home.html", {})


def order(request):
    # Handling a POST request
    if request.method == "POST":
        # Capture all the information of the POST request into a `PizzaForm` instance
        filled_form = PizzaForm(request.POST)
        if filled_form.is_valid():
            note = "Thanks for ordering! You %s with %s and %s is on it's way" % (
                filled_form.cleaned_data["size"],
                filled_form.cleaned_data["topping1"],
                filled_form.cleaned_data["topping2"],
                )
            # note = f"Thanks for ordering! You {filled_form.cleaned_data["size"]} with {filled_form.cleaned_data["topping1"]} and {filled_form.cleaned_data["topping2"]} is on its way"

            new_form = PizzaForm()
            return render(request, "pizza/order.html", {"pizzaform": new_form, "note": note})
    # Handling the rest of http methods
    else:
        form = PizzaForm()
        return render(request, "pizza/order.html", {"pizzaform": form})
