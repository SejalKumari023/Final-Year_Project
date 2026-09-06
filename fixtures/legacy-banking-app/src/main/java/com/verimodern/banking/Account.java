package com.verimodern.banking;

public class Account {
    private int balance;

    public Account(int openingBalance) {
        this.balance = openingBalance;
    }

    public int withdraw(int amount) {
        if (amount <= 0 || amount > balance) {
            throw new IllegalArgumentException("Invalid withdrawal amount");
        }
        balance -= amount;
        return balance;
    }

    public int getBalance() {
        return balance;
    }
}
