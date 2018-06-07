# Pranav_Insight_Repo

### Code Flow ###

We concatenate date and time after discerning the correct header indices. Here it does not seem that the unique document identifier is relevant.

Parsing begins line by line; for the first line of input we initialize the following three data structures:

master_dict: An ordered dictionary used to store the latest timestamp of a user's session

requests_dict: An unordered dictionary used to store the number of requests made during a particular user's session

session_start_dict: An ordered dictionary used to store the beginning of a user session

Logic: For each line, the current timestamp is compared to the latest timestamp previously encountered. This is done by comparing to the last entry in master_dict.
If the current line signifies the start of a new user session, the information is stored in the 3 dicts.
If the current line ip is already present, the timestamp in master_dict is updated and the number of requests is incremented.

If the current timestamp is later than the previous latest timestamp, we begin checking for inactivitiy periods from the start of master_dict. Once an entry is encountered which is still an active session we stop checking as this dict is ordered by time.

Lastly, we flush the remaining existing sessions once the end of file is reached. session_start_dict maintains the order matching the input file order.



