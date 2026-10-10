from ErisPulse.Core.Bases import Field, Model


class Reminder(Model):

    __tablename__ = "reminders"

    id: int = Field(primary_key=True, autoincrement=True)
    platform: str = Field(max_length=64)
    target_type: str = Field(max_length=8, choices=["user", "group"])
    target_id: str = Field(max_length=128)
    user_id: str = Field(max_length=128)
    due_at: float = Field(index=True)
    text: str = Field(max_length=500)
    status: str = Field(max_length=8, choices=["pending", "done", "canceled"], default="pending")
    created_at: float = Field(default=0)
