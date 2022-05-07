from django.shortcuts import render, redirect
from .models import *
from .forms import *

def home(request):
    variables = Variable.objects.all()
    for x in variables:
        y = x.values()
    return render(request, 'home.html', {'variables': variables})

def projection(request):
    variables = Variable.objects.all()
    period = Global.objects.all().first().projection_period
    headings = ["Time",]
    formulae = ["", ]
    for x in variables:
        headings.append(x.name)
        formulae.append(x.formula)

    grid = [["" for x in range(variables.count() + 1)] for y in range(period)]

    # Add time period to first column
    for y in range(period): grid[y][0] = y

    # Add values to grid
    x = 1
    for variable in variables:
        values = variable.values_round()
        y = 0
        for value in values:
            grid[y][x] = value
            y += 1
        x += 1
    return render(request, 'projection.html', {'headings': headings, 'period': period, 'grid': grid, 'formulae': formulae})

def new_variable(request):
    if request.method == 'POST':
        form = VariableForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = VariableForm
        form.fields['formula'].disabled = True
    return render(request, 'new_variable.html', {'form':form})

def edit_variable(request, id):
    variable = Variable.objects.get(id=id)
    form = VariableForm(request.POST or None, instance=variable)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request,'new_variable.html',{'form':form})

def delete_variable(request, id):
    variable = Variable.objects.get(id=id)
    variable.delete()
    return redirect("home")

def create_levels():
    variables = Variable.objects.all()
    variables.update(level=None)
    variables = list(variables)
    all_found = False
    while not all_found:
        all_found = True
        for x in variables:
            # Does the variable have a level?
            if not x.level:
                # Which variables does it reference?
                referenced_variables = []
                for y in variables:
                    found = x.formula.find(y.name)
                    if found != -1: referenced_variables.append(y)
                # Does it reference other variables?
                if len(referenced_variables) == 0:
                    x.level = 0
                    x.save()
                else:
                    # Do all of those variables have a level
                    all_referenced_variables_have_level = True
                    max_level = 0
                    for z in referenced_variables:
                        if z.level is None:
                            all_referenced_variables_have_level = False
                            all_found = False
                        else:
                            max_level = max(max_level, z.level)
                    if all_referenced_variables_have_level:
                        x.level = max_level + 1
                        x.save()


            for y in variables:
                if x != y:
                    found = x.formula.find(y.name)
    return
