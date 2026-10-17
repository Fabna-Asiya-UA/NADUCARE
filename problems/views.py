
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.views.decorators.http import require_POST

from .models import Problem
from .forms import ProblemForm

from solutions.models import Solution, SolutionVote
from solutions.forms import SolutionForm


def home(request):
    latest_problems = Problem.objects.order_by('-created_at')[:6]

    context = {
        'latest_problems': latest_problems,
        'total_problems': Problem.objects.count(),
        'resolved_problems': Problem.objects.filter(
            status=Problem.Status.RESOLVED
        ).count(),
    }

    return render(request, 'home.html', context)


def problem_list(request):
    problems = Problem.objects.order_by('-created_at')

    district = request.GET.get('district', '')
    category = request.GET.get('category', '')
    search = request.GET.get('search', '').strip()

    # Filter by a valid district
    if district in dict(Problem.DISTRICTS):
        problems = problems.filter(district=district)

    # Filter by a valid category
    if category in Problem.Category.values:
        problems = problems.filter(category=category)

    # Search by title, description, or location
    if search:
        problems = problems.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(location__icontains=search)
        )

    context = {
        'problems': problems,
        'districts': Problem.DISTRICTS,
        'categories': Problem.Category.choices,
        'selected_district': district,
        'selected_category': category,
        'search': search,
    }

    return render(request, 'problems/problem_list.html', context)


def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)

    # Display solutions with the highest vote count first
    solutions = (
        Solution.objects.filter(problem=problem)
        .annotate(vote_count=Count('votes'))
        .select_related('user')
        .order_by('-vote_count', '-created_at')
    )

    user_voted_ids = []

    # Find which solutions the current user has voted for
    if request.user.is_authenticated:
        user_voted_ids = list(
            SolutionVote.objects.filter(
                user=request.user,
                solution__problem=problem
            ).values_list('solution_id', flat=True)
        )

    context = {
        'problem': problem,
        'solutions': solutions,
        'solution_form': SolutionForm(),
        'user_voted_ids': user_voted_ids,
    }

    return render(
        request,
        'problems/problem_detail.html',
        context
    )


@login_required
def create_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST, request.FILES)

        if form.is_valid():
            problem = form.save(commit=False)
            problem.user = request.user
            problem.save()

            messages.success(
                request,
                'Problem reported successfully!'
            )

            return redirect('problem_detail', pk=problem.pk)

        messages.error(
            request,
            'Please correct the errors in the form.'
        )

    else:
        form = ProblemForm()

    return render(
        request,
        'problems/problem_form.html',
        {'form': form}
    )


@login_required
@require_POST
def add_solution(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    form = SolutionForm(request.POST)

    if form.is_valid():
        solution = form.save(commit=False)
        solution.problem = problem
        solution.user = request.user
        solution.save()

        messages.success(
            request,
            'Your solution was submitted!'
        )
    else:
        messages.error(
            request,
            'Please enter a valid solution.'
        )

    return redirect('problem_detail', pk=problem.pk)


@login_required
@require_POST
def vote_solution(request, pk):
    solution = get_object_or_404(
        Solution.objects.select_related('problem'),
        pk=pk
    )

    vote, created = SolutionVote.objects.get_or_create(
        solution=solution,
        user=request.user
    )

    if created:
        messages.success(request, 'Your vote was recorded.')
    else:
        vote.delete()
        messages.info(request, 'Your vote was removed.')

    return redirect(
        'problem_detail',
        pk=solution.problem_id
    )
