package com.verimodern.banking;

import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class AccountTest {
    @Test
    public void withdrawReducesBalance() {
        Account account = new Account(1000);

        assertEquals(750, account.withdraw(250));
        assertEquals(750, account.getBalance());
    }

    @Test(expected = IllegalArgumentException.class)
    public void withdrawRejectsAmountAboveBalance() {
        new Account(100).withdraw(101);
    }
}
