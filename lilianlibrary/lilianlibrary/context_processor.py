from catalog.models import Quote
from random import sample

# Used for displaying random quotes in left menu
def quote_generator(request):
    # Counts the number of quotes in database
    total_quotes = Quote.objects.all().count()
    # Prevent crashes if there is no quotes
    if total_quotes == 0:
        return {'random_quote': ''}
    # Gets a random number that does not exceed the number of avialable
    random_id = sample(range(1, total_quotes), 1)
    # Filter a quote by a randomized id number
    random_quote = Quote.objects.filter(id__in=random_id)
    # This variable is available in all views
    return {'random_quote': random_quote}
