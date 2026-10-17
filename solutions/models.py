from django.db import models
from django.contrib.auth.models import User
from problems.models import Problem


class Solution(models.Model):
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name='solutions'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submitted_solutions'
    )

    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Solution for {self.problem.title}'


class SolutionVote(models.Model):
    solution = models.ForeignKey(
        Solution,
        on_delete=models.CASCADE,
        related_name='votes'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='solution_votes'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['solution', 'user'],
                name='unique_user_solution_vote'
            )
        ]

    def __str__(self):
        return f'{self.user.username} voted for solution {self.solution_id}'