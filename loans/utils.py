import decimal
from datetime import datetime, timedelta

from loans.constants import LOAN_STATE_PAID


def get_loan_repayment_date_and_term(total_amount, term):
    date_and_amount = []
    repayment_amount = round(total_amount / term, 2)
    time_now = datetime.now()
    for period in range(1, term + 1):
        repayment_date = time_now + timedelta(weeks=period)
        if period == term:
            repayment_amount = total_amount - (repayment_amount * (term - 1))
        date_and_amount.append((repayment_date, repayment_amount))
    return date_and_amount


def is_repayment_complete(repayment):
    return repayment.amount == repayment.amount_paid


def get_repayment_amount(repayment, amount):
    if amount >= repayment.amount - repayment.amount_paid:
        return repayment.amount - repayment.amount_paid
    return amount


def update_pending_repayments(pending_repayments, remaining_amount):
    for pending_repayment in pending_repayments:
        if remaining_amount == decimal.Decimal(0):
            break
        repayment_amount = get_repayment_amount(pending_repayment, remaining_amount)
        pending_repayment.amount_paid += repayment_amount
        remaining_amount -= repayment_amount
        if is_repayment_complete(pending_repayment):
            pending_repayment.state = LOAN_STATE_PAID
        pending_repayment.save()
