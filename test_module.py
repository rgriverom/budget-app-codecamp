from unittest import TestCase, main

from budget import create_spend_chart, Category


class TestBudgetApp(TestCase):
    def setUp(self):
        self.food = Category("Food")
        self.family = Category("Family")
        self.workers = Category("Workers")

    def test_deposit(self):
        self.food.deposit(900, "deposit")
        current = self.food.ledger[0]
        expected = {"amount": 900, "description": "deposit"}
        self.assertEqual(
            current, expected, "Expected:\n {} \n Gets:\n {}".format(expected, current)
        )

    def test_deposit_no_description(self):
        self.food.deposit(45.56)
        current = self.food.ledger[0]
        expected = {"amount": 45.56, "description": ""}
        self.assertEqual(
            current, expected, "Expected:\n {} \n Gets:\n {}".format(expected, current)
        )

    def test_withdraw(self):
        self.food.deposit(900, "deposit")
        self.food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
        current = self.food.ledger[1]
        expected = {"amount": -45.67, "description": "milk, cereal, eggs, bacon, bread"}
        self.assertEqual(
            current, expected, "Expected:\n {} \n Gets:\n {}".format(expected, current)
        )

    def test_withdraw_no_description(self):
        self.food.deposit(900, "deposit")
        good_withdraw = self.food.withdraw(45.67)
        current = self.food.ledger[1]
        expected = {"amount": -45.67, "description": ""}
        self.assertEqual(
            current, expected, "Expected:\n {} \n Gets:\n {}".format(expected, current)
        )
        self.assertEqual(good_withdraw, True,
                         "Expected:\n {} \n Gets:\n {}".format(True, good_withdraw))

    def test_get_balance(self):
        self.food.deposit(900, "deposit")
        self.food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
        current = self.food.get_balance()
        expected = 854.33
        self.assertEqual(
            current, expected, "Expected:\n {} \n Gets:\n {}".format(expected, current)
        )

    def test_transfer(self):
        self.food.deposit(900, "deposit")
        self.food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
        good_transfer = self.food.transfer(20, self.family)
        current = self.food.ledger[2]
        expected = {"amount": -20, "description": "Transfer to Family"}
        self.assertEqual(current, expected,
                         'Expected `transfer` method to create a specific ledger item in food object.')
        self.assertEqual(good_transfer, True, 'Expected `transfer` method to return `True`.')
        current = self.family.ledger[0]
        expected = {"amount": 20, "description": "Transfer from Food"}
        self.assertEqual(
            current, expected, "Expected:\n {} \n Gets:\n {}".format(expected, current)
        )

    def test_check_funds(self):
        self.food.deposit(10, "deposit")
        current = self.food.check_funds(20)
        expected = False
        self.assertEqual(
            current, expected, "Expected:\n {} \n Gets:\n {}".format(expected, current)
        )
        current = self.food.check_funds(10)
        expected = True
        self.assertEqual(
            current, expected, "Expected:\n {} \n Gets:\n {}".format(expected, current)
        )

    def test_withdraw_no_funds(self):
        self.food.deposit(100, "deposit")
        good_withdraw = self.food.withdraw(100.10)
        self.assertEqual(good_withdraw, False, 'Expected `withdraw` method to return `False`.')

    def test_transfer_no_funds(self):
        self.food.deposit(100, "deposit")
        good_transfer = self.food.transfer(200, self.family)
        self.assertEqual(good_transfer, False, 'Expected `transfer` method to return `False`.')

    def test_to_string(self):
        self.food.deposit(900, "deposit")
        self.food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
        self.food.transfer(20, self.family)
        current = str(self.food)
        expected = f"*************Food*************\ndeposit                 900.00\nmilk, " \
                   f"cereal, eggs, bac -45.67\nTransfer to Family      -20.00\nTotal: 834.33"
        self.assertEqual(
            current, expected, "Expected:\n {} \n Gets:\n {}".format(expected, current)
        )

    def test_create_spend_chart(self):
        self.food.deposit(900, "deposit")
        self.family.deposit(900, "deposit")
        self.workers.deposit(900, "deposit")
        self.food.withdraw(105.55)
        self.family.withdraw(33.40)
        self.workers.withdraw(10.99)
        current = create_spend_chart([self.workers, self.food, self.family])
        expected = "Percentage spent by category\n100|          \n 90|          \n 80|          " \
                   "\n 70|    o     \n 60|    o     \n 50|    o     \n 40|    o     \n 30|    o     \n 20|    o  o  \n 10|    o  o  \n  0| o  o  o  \n    ----------\n     W  F  F  \n     o  o  a  \n     r  o  m  \n     k  d  i  \n     e     l  \n     r     y  \n     s        "
        self.assertEqual(
            current, expected, "Expected:\n {} \n Gets:\n {}".format(expected, current)
        )


if __name__ == "__main__":
    main()
