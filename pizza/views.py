from django.shortcuts import render
from .forms import PizzaForm, MultiplePizzaForm
from django.forms import formset_factory

from .models import Pizza


def home(request):
    return render(request, "pizza/home.html", {})


def order(request):
    # Make a form set
    multiple_form = MultiplePizzaForm()

    # Handling a POST request
    if request.method == "POST":
        # Capture all the information of the POST request into a `PizzaForm` instance
        filled_form = PizzaForm(request.POST)

        # If `filled_form` is valid
        if filled_form.is_valid():
            # Save the object
            created_pizza = filled_form.save()
            # Id of the order
            created_pizza_pk = created_pizza.id

            # Make a message with the form information
            note = "Thanks for ordering! You %s with %s and %s is on it's way" % (
                filled_form.cleaned_data["size"],
                filled_form.cleaned_data["topping1"],
                filled_form.cleaned_data["topping2"],
            )

            # Make a new form
            new_form = PizzaForm()
            # Render the order template and pass the new form and the message
            return render(
                request,
                "pizza/order.html",
                {
                    "created_pizza_pk": created_pizza_pk,
                    "pizzaform": new_form,
                    "note": note,
                    "multiple_form": multiple_form,
                },
            )
    # Handling the rest of http methods
    else:
        form = PizzaForm()
        return render(
            request,
            "pizza/order.html",
            {"pizzaform": form, "multiple_form": multiple_form},
        )


def pizzas(request):
    number_of_pizzas = 2
    filled_multiple_pizza_form = MultiplePizzaForm(request.GET)

    if filled_multiple_pizza_form.is_valid():
        number_of_pizzas = filled_multiple_pizza_form.cleaned_data["number"]

    # Class that hold the formset
    PizzaFormSet = formset_factory(PizzaForm, extra=number_of_pizzas)
    # Base form set
    formset = PizzaFormSet()

    # Handle POST requests
    if request.method == "POST":
        # Fill a formset with the request data
        filled_formset = PizzaFormSet(request.POST)

        # If the formset is valid
        if filled_formset.is_valid():
            # Print the topping 1 of all forms
            for form in filled_formset:
                print(form.cleaned_data["topping1"])
            # Note of success
            note = "Pizzas have been orderer!"

        # If the formset is invalid
        else:
            # Note of error
            note = "Order has not created, please try again."

        return render(request, "pizza/pizzas.html", {"note": note, "formset": formset})
    # Handle non-POST requests
    else:
        return render(request, "pizza/pizzas.html", {"formset": formset})


def edit_order(request, pk):
    # Get the order from db
    pizza = Pizza.objects.get(pk=pk)
    # Make a form fill with the order data
    form = PizzaForm(instance=pizza)

    # Handle POST requests
    if request.method == "POST":
        # Make a new form with the new order data
        filled_form = PizzaForm(request.POST, instance=pizza)

        if filled_form.is_valid():
            # Save the new object
            filled_form.save()
            # Replace the past form with new
            form = filled_form
            # Success message
            note = "Order has been updated."

            return render(
                request,
                "pizza/edit_order.html",
                {"note": note, "pizzaform": form, "pizza": pizza},
            )
    # Handle non-POST requests
    else:
        return render(
            request, "pizza/edit_order.html", {"pizzaform": form, "pizza": pizza}
        )
