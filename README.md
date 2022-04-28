## DMV Appointment - Expectations

* Include a `README` with:
  * Instructions to run the code and install any necessary dependencies.
    
    :pip install python
    :python libraries 
       json
       itertools
       seaborn
  
  * Description of the problem and solution.
    
    Problem: We need to process all customers in an efficient process so the tellers can go home early.
    Solution: Match the teller with customer type so we can use the multiplier to reduce wait time for the customer. Less wait time equals happy customer.

  * Reasoning behind your technical choices.
    
    We can only work with the data thats available and given, but we can manipulate the data to do different
    technical choices.

  * If there are features you didn't have time to implement or would improve or do differently next time, describe the intended behavior.

    
    Now the data has been processed and aggregated. We can do diffrent features to imporve the process.
    For example, we can do anomaly detection to see which tellers have more appointments than other tellers.
    Then we can remove the additional appointments from the outliers to the other tellers that have less appointments and total time.



