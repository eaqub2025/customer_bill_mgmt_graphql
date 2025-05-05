from django.db import models


class CustomerBillStateType(models.TextChoices):
    NEW = "new", "New"
    ONHOLD = "onHold", "On Hold"
    VALIDATED = "validated", "Validated"
    SENT = "sent", "Sent"
    PARTIALLY_PAID = "partiallyPaid", "Partially Paid"
    SETTLED = "settled", "settled"


class CustomerBillRunType(models.TextChoices):
    ON_CYCLE = "onCycle", "On Cycle"
    OFF_CYCLE = "offCycle", "Off Cycle"


class BaseModel(models.Model):
    """
    Base model with baseType, type and schemaLocation. Will be inherited in all other models if required.
    """

    base_type = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    schema_location = models.CharField(max_length=100)

    class Meta:
        abstract = True


class CustomerBill(BaseModel):
    href = models.CharField(max_length=100, unique=True)
    bill_date = models.DateTimeField(blank=True, null=True)
    bill_no = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)
    next_bill_date = models.DateTimeField(blank=True, null=True)
    payment_due_date = models.DateTimeField(blank=True, null=True)
    run_type = models.CharField(max_length=50, choices=CustomerBillRunType.choices, blank=True, null=True)
    amount_due = models.ForeignKey(
        'Money', on_delete=models.SET_NULL, related_name='customerbill_amountdue', blank=True, null=True
    )
    billing_account = models.ForeignKey('BillingAccountRef', on_delete=models.SET_NULL, blank=True, null=True)
    billing_period = models.ForeignKey('TimePeriod', on_delete=models.SET_NULL, blank=True, null=True)
    financial_account = models.ForeignKey('FinancialAccountRef', on_delete=models.SET_NULL, blank=True, null=True)
    payment_method = models.ForeignKey('paymentMethodRef', on_delete=models.SET_NULL, blank=True, null=True)
    remaining_amount = models.ForeignKey(
        'Money', on_delete=models.SET_NULL, related_name='customerbill_remaining_amount', blank=True, null=True
    )
    state = models.CharField(max_length=50, choices=CustomerBillStateType.choices, blank=True, null=True)
    tax_excluded_amount = models.ForeignKey(
        'Money', on_delete=models.SET_NULL, related_name='customerbill_tax_excluded', blank=True, null=True
    )
    tax_included_amount = models.ForeignKey(
        'Money', on_delete=models.SET_NULL, related_name='customerbill_tax_included', blank=True, null=True
    )

    class Meta:
        verbose_name_plural = 'customer_bill'
        db_table = 'customer_bill'

    def appliedPayment(self):
        return self.applied_payments

    def relatedParty(self):
        return self.related_parties

    def billDocument(self):
        return self.bill_documents

    def taxItem(self):
        return self.tax_items


class Money(models.Model):
    unit = models.CharField(max_length=10, blank=True, null=True)
    value = models.DecimalField(default=0, max_digits=50, decimal_places=2)

    class Meta:
        verbose_name_plural = 'money'
        db_table = 'money'


class AppliedPayment(BaseModel):
    customer_bill = models.ForeignKey(
        'CustomerBill', on_delete=models.SET_NULL, related_name='applied_payments', blank=True, null=True
    )
    applied_amount = models.ForeignKey('Money', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('PaymentRef', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'applied_payment'
        db_table = 'applied_payment'


class AttachmentRefOrValue(BaseModel):
    customer_bill = models.ForeignKey(
        'CustomerBill', on_delete=models.SET_NULL, related_name='bill_documents', blank=True, null=True
    )
    href = models.CharField(max_length=100, blank=True, null=True)
    attachment_type = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    mime_type = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    size = models.ForeignKey('Quantity', on_delete=models.SET_NULL, blank=True, null=True)
    valid_for = models.ForeignKey('TimePeriod', on_delete=models.SET_NULL, blank=True, null=True)
    referred_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'attachment_ref_or_value'
        db_table = 'attachment_ref_or_value'


class BillingAccountRef(BaseModel):
    id = models.CharField(max_length=100, primary_key=True, unique=True)
    href = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    referred_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'billing_account_ref'
        db_table = 'billing_account_ref'


class TimePeriod(models.Model):
    end_date_time = models.DateTimeField(blank=True, null=True)
    start_date_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'time_period'
        db_table = 'time_period'


class FinancialAccountRef(BaseModel):
    id = models.CharField(max_length=100, primary_key=True, unique=True)
    href = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    referred_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'financial_account_ref'
        db_table = 'financial_account_ref'

    def accountBalance(self):
        return self.account_balances


class PaymentMethodRef(BaseModel):
    id = models.CharField(max_length=100, primary_key=True, unique=True)
    href = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    referred_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'payment_method_ref'
        db_table = 'payment_method_ref'


class PaymentRef(BaseModel):
    id = models.CharField(max_length=100, primary_key=True, unique=True)
    href = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100)
    referred_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'payment_ref'
        db_table = 'payment_ref'


class TaxItem(BaseModel):
    customer_bill = models.ForeignKey(
        'CustomerBill', on_delete=models.SET_NULL, related_name='tax_items', blank=True, null=True
    )
    tax_category = models.CharField(max_length=100, blank=True, null=True)
    tax_rate = models.DecimalField(max_digits=50, decimal_places=2)
    tax_amount = models.ForeignKey('Money', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'tax_item'
        db_table = 'tax_item'


class Quantity(models.Model):
    amount = models.DecimalField(default=1, max_digits=50, decimal_places=2)
    units = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'quantity'
        db_table = 'quantity'


class AccountBalance(BaseModel):
    account_ref = models.ForeignKey(
        'FinancialAccountRef', on_delete=models.SET_NULL, related_name='account_balances', blank=True, null=True
    )
    balance_type = models.CharField(max_length=50)
    valid_for = models.ForeignKey('TimePeriod', on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.ForeignKey('Money', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'account_balance'
        db_table = 'account_balance'


class RelatedPartyRef(BaseModel):
    customer_bill = models.ForeignKey(
        'CustomerBill', on_delete=models.SET_NULL, related_name='related_parties', blank=True, null=True
    )
    id = models.CharField(max_length=100, primary_key=True, unique=True)
    href = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    referred_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'related_party_ref'


class ConfigValue(models.Model):
    attribute_name = models.CharField(max_length=200, blank=False, null=False)
    value = models.CharField(max_length=200, blank=False, null=False)
    schema_name = models.CharField(max_length=200, blank=True, null=True)
    base_app = models.CharField(max_length=200, blank=True, null=True)
    service_name = models.CharField(max_length=200, blank=False, null=False)
    base_type = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    schema_location = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Config values"
        db_table = "config_value"


class AccountBillStatus(models.Model):
    account_id = models.CharField(max_length=128, blank=False, null=False, db_index=True)
    bill_id = models.CharField(max_length=128, blank=False, null=False, db_index=True)
    bill_status = models.CharField(max_length=128, blank=False, null=False)
    crated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'account_bill_status'
        verbose_name_plural = 'Account Bill Status'
