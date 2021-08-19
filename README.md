#Simple command-line utility for querying BonusWay campaigns

To install the utility, use

```
pip install .
```

And to run it:

```
python3 -m python_task
```

##Additional features

By default, the program will query the `https://static-api.prod.bonusway.com/api/16/campaigns_limit_{limit}_offset_{offset}_order_popularity.json` api endpoint (where {limit} and {offset} are integers)
and filter out all items whose commission is not in percent or is less-or-equal to 2.25 and
then display remaining titles in alphabetical order.

It is, however, possible to change both the filter condition, the sorting condition
and the print-string. To see the possible parameters to the program:


```
python3 -m python_task -h
```

The filter and sort conditions can be specified using arbitrary python expression (limited to booleans and arithmetic operators).
The print-string is a python format string such as `"{title} - {description}"` and is
applied to each individual item with a newline printed between items.

For example, the default behaviour is equivalent to:

```
python3 -m python_task -f "commission.max.amount > 2.25 and commission.max.unit == '%'" -s "title.lower()" -p "{title}"
```

Note that it is possible to use dot-notation instead of subscripts in the expressions (subscripts work too!).
Also note that it is possible to access methods such as `lower()` in the expression (here used to avoid case-sensitive sorting).
## Caching

By default, the files received from the remote api are cached locally. If you want to clear the 
cache (forcing the program to use the remote api again), use `--clear`:

```
python3 -m python_task --clear
```
