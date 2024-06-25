from datetime import datetime, timedelta


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
