# Notification System & Staff Self-Service Enhancements

## Overview
Add notification system with bell icon + dropdown + full page. Enable staff to mark leave and request advance from their own profile.

## 1. Notification Model (new `notifications` app)

### `Notification`
- `recipient` — FK to `User`, related_name='notifications'
- `title` — CharField(200)
- `message` — TextField(blank)
- `type` — CharField(20), choices: task_assigned, task_overdue, salary_reminder, reminder_due
- `link` — CharField(200, blank), URL to relevant page
- `is_read` — BooleanField(default=False)
- `created_at` — DateTimeField(auto_now_add=True)

Meta: ordering = ['-created_at']

## 2. Notification Generation

### Signals (auto)
- `post_save` on `AssignedTask` → notification to staff: "Task '{name}' assigned on {date}"
- `post_save` on `Reminder` when due_date is today → notification to admin (checked on-demand too)

### On-Demand Checks (run when notification page loads)
- **Overdue tasks**: tasks past assigned_date, not completed → create notifications if not exist
- **Salary reminders**: salary_date approaching within 3 days, not yet paid → notify admin
- **Upcoming reminders**: due_date within 3 days, not completed → notify admin

De-duplication: check `Notification.objects.filter(type=..., recipient=..., created_at__date=today)` before creating.

## 3. Display

### Bell Icon in Top Bar (base.html)
- Right side, before greeting
- Shows bell icon with badge (unread count in red circle)
- Click opens dropdown with 5 most recent notifications
- Each item: icon by type, title, time ago, link
- "Mark all read" link at bottom
- "View all" link to full page

### Notification Page (`/notifications/`)
- Table/filtered list of all notifications
- Filter by type buttons
- Mark as read toggle
- "Mark All Read" button
- Color-coded by type

## 4. Views

- `notification_list` — GET: render list with all user notifications, triggers on-demand checks
- `notification_mark_read` — POST: toggle `is_read` on single notification, returns JSON
- `notification_mark_all_read` — POST: marks all user's notifications as read, returns JSON

## 5. Context Processor

`notifications/context_processors.py`:
```python
def notifications(request):
    if request.user.is_authenticated:
        return {
            'unread_count': Notification.objects.filter(recipient=request.user, is_read=False).count(),
            'recent_notifications': Notification.objects.filter(recipient=request.user)[:5],
        }
    return {}
```

## 6. Staff Self-Service: Leave & Advance on Own Profile

- `my_profile` view: set `readonly` only for edit button, NOT for leave/advance
- `staff_detail.html`: show "Mark Leave" and "Request Advance" buttons even in readonly mode
- These are self-service actions (staff manages their own leaves/advances)

## 7. Files

| File | Action |
|------|--------|
| `notifications/models.py` | Create — Notification model |
| `notifications/views.py` | Create — list, mark_read, mark_all_read |
| `notifications/urls.py` | Create — URL patterns |
| `notifications/apps.py` | Create — AppConfig |
| `notifications/admin.py` | Create — admin registration |
| `notifications/context_processors.py` | Create — unread count + recent |
| `notifications/signals.py` | Create — task_assigned signal |
| `templates/notifications/list.html` | Create — full notification page |
| `templates/base.html` | Modify — bell icon + dropdown |
| `staff/templates/staff/staff_detail.html` | Modify — show leave/advance in readonly |
| `home_organizer/settings.py` | Modify — register app + context processor |
| `home_organizer/urls.py` | Modify — include notifications URLs |
