from django.contrib.auth.models import User
from django.db import transaction
from datetime import datetime
from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(tickets: list, username: str, date: str) -> Order:
    user = User.objects.get(username=username)
    if date:
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order = Order.objects.create(user=user, created_at=created_at)
    else:
        order = Order.objects.create(user=user)

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket_data["movie_session"]
        )
        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )
    return order


def get_orders(username: str) -> list:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
