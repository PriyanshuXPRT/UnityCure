from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def telecon_room(request, room_name: str):
    """Render a simple WebRTC + chat room page."""
    role = getattr(request.user, "role", "PATIENT").lower()
    return render(request, "telecon/room.html", {"room_name": room_name, "role": role})
