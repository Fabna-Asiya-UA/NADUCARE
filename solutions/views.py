from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from problems.models import Problem
from .models import Solution, SolutionVote
from .forms import SolutionForm


@login_required
def add_solution(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)

    if request.method == 'POST':
        form = SolutionForm(request.POST)

        if form.is_valid():
            solution = form.save(commit=False)
            solution.problem = problem
            solution.user = request.user
            solution.save()

            messages.success(request, 'Your solution was added.')
        else:
            for error in form.errors.values():
                messages.error(request, ' '.join(error))

    return redirect('problem_detail', pk=problem.pk)


@login_required
def vote_solution(request, solution_id):
    solution = get_object_or_404(Solution, pk=solution_id)

    if request.method == 'POST':
        if solution.user == request.user:
            messages.error(request, 'You cannot vote for your own solution.')
        else:
            vote, created = SolutionVote.objects.get_or_create(
                solution=solution,
                user=request.user
            )

            if created:
                messages.success(request, 'Your vote has been recorded.')
            else:
                vote.delete()
                messages.info(request, 'Your vote has been removed.')

    return redirect('problem_detail', pk=solution.problem.pk)