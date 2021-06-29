import random
from abc import ABC, abstractmethod

from payment_service.app.api.models import Payment
from risk_engine_service.models import ProcessedPayment


class AbstractRiskEngine(ABC):
    """ Base abstract class for other RiskEngine implementation, should be used as an interface. """

    @abstractmethod
    def compute_risk_score(self, payment: Payment) -> float:
        pass

    @abstractmethod
    def approve_payment(self, payment: Payment, risk_score: float) -> ProcessedPayment:
        pass

    def process(self, payment: Payment) -> ProcessedPayment:
        """
        This method applies the payment processing logic on an input payment:
        1. Compute the risk score
        2. Check payment approval

        :param payment: Input Payment object
        :return: The output ProcessedPayment object
        """
        risk_score = self.compute_risk_score(payment)
        processed_payment = self.approve_payment(payment, risk_score)
        return processed_payment


class RandomRiskEngine(AbstractRiskEngine):
    """ Dummy implementation for RiskEngine, can be used for testing purposes. """

    def __init__(self, min_value: float, max_value: float, approval_threshold: float):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value
        self.approval_threshold = approval_threshold

    def compute_risk_score(self, payment: Payment) -> float:
        """ Randomly chooses a float between min_value and max_value, then rounds to first two decimals. """
        return round(random.uniform(self.min_value, self.max_value), 2)

    def approve_payment(self, payment: Payment, risk_score: float) -> ProcessedPayment:
        """ Checks if risk score is below the approval_threshold. """
        approval = risk_score <= self.approval_threshold
        return ProcessedPayment(
            payment=payment,
            risk_score=risk_score,
            is_approved=approval,
        )
