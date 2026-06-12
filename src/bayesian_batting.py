from scipy.stats import beta

#validation functions for inputs
def validate_batting_statistics(hits: int, at_bats: int) -> None:
    if at_bats <= 0:
        raise ValueError("at_bats must be positive, there is no point in calculating average for 0 at bats")
    if hits < 0:
        raise ValueError("It is impossible to have a negative number of hits")
    if hits > at_bats:
        raise ValueError("This can't be the case, you can't have more hits then at bats")
    
def validate_beta_distribution_inputs(alpha: int, beta: int) -> None:
    if alpha <= 0:
        raise ValueError("A hitters previous hits cannot be less than or equal to zero")
    if beta <= 0:
        raise ValueError("A hitters previous at bats cannot be less than or equal to zero")
    
def validate_confidence_inputs(confidence: float) -> None:
    if confidence >= 1:
        raise ValueError("Confidence must be less than 1")
    if confidence <= 0:
        raise ValueError("Confidence cannot be zero or less")
    
#calculation functions for naive average
    
def naive_average(hits: int, at_bats: int) -> float:
    
    validate_batting_statistics(hits, at_bats)
    
    return hits / at_bats

def calculate_outs(hits: int, at_bats: int) -> int:

    validate_batting_statistics(hits, at_bats)

    return (at_bats - hits)


#for later use in beta distribution, these are the beta parameters:
#this is for the prior part of the distribution, i.e. the hitters previous stats
prior_alpha = 25
prior_beta = 75

#this calculates the posterior parameters, that being the output of the bayesian formula
#so, adding the 'new' data to the 'known' data, by adding the new hits to the existing hits and the new ABs to the existing ABs

def posterior_parameters(prior_alpha: int, prior_beta: int, hits: int, at_bats: int) -> tuple[int, int]:

    #firstly, lets validate the inputs
    validate_batting_statistics(hits, at_bats)
    validate_beta_distribution_inputs(prior_alpha, prior_beta)

    #now let's calculate the new posterior parameters for the beta distribution
    posterior_alpha = prior_alpha + hits
    posterior_beta = prior_beta + at_bats

    return posterior_alpha, posterior_beta

#this outputs the mean of the posterior distribution, the most accurate 'one-number' statistic of the bayesian batting average
def calculate_posterior_mean(hits: int, at_bats: int, prior_alpha: int, prior_beta: int) -> float:

    posterior_alpha, posterior_beta = posterior_parameters(prior_alpha, prior_beta, hits, at_bats)

    return posterior_alpha / (posterior_alpha + posterior_beta)

#this outputs the mean of the prior distribution, the most accurate 'one-number' statistic of the bayesian average before adding the new data
def calculate_prior_mean(posterior_alpha: int, posterior_beta: int) -> float:
    
    validate_beta_distribution_inputs(posterior_alpha, posterior_beta)

    return posterior_alpha / (posterior_alpha + posterior_beta)

#remember: the returned average is as a distribution, not a single value
#this function outputs the standard deviation of the distribution
def calculate_posterior_std(posterior_alpha: int, posterior_beta: int) -> float:
    validate_beta_distribution_inputs(posterior_alpha, posterior_beta)
    return beta.std(posterior_alpha, posterior_beta)

#this function outputs a confidence interval from the 5th percentile to the 95th, i.e. very confidently says the true average is somewhere in here
def calculate_posterior_confidence_interval(
        hits: int,
        at_bats: int,
        prior_alpha: int,
        prior_beta: int,
        confidence: float = 0.95
    ) -> tuple[float, float]:

    validate_confidence_inputs(confidence)

    #find the beta distribution we're working with
    posterior_alpha, posterior_beta = posterior_parameters(prior_alpha, prior_beta, hits, at_bats)

    #find the upper and lower tails for the confidence score given
    lower_tail = (1 - confidence) / 2
    upper_tail = 1 - lower_tail

    #find what average is at the lower/upper tail of the beta distribution
    lower = beta.ppf(lower_tail, posterior_alpha, posterior_beta)
    upper = beta.ppf(upper_tail, posterior_alpha, posterior_beta)

    return lower, upper

#final summary function that summarises/finds all calculations for one input/player
#makes experiments easier

def batting_summary(hits: int, at_bats: int, prior_alpha: int, prior_beta: int) -> dict:

    #calculate required statistics
    naive_batting_average = naive_average(hits, at_bats)

    posterior_mean = calculate_posterior_mean(hits, at_bats, prior_alpha, prior_beta)

    posterior_alpha, posterior_beta = posterior_parameters(prior_alpha, prior_beta, hits, at_bats)
    posterior_standard_deviation = calculate_posterior_std(prior_alpha, prior_beta)

    lower, upper = calculate_posterior_confidence_interval(hits, at_bats, prior_alpha, prior_beta)

    return {
        "hits": hits,
        "at_bats": at_bats,
        "naive_average": naive_batting_average,
        "posterior_alpha": posterior_alpha,
        "posterior_beta": posterior_beta,
        "posterior_mean": posterior_mean,
        "posterior_std": posterior_standard_deviation,
        "credible_interval_lower": lower,
        "credible_interval_upper": upper,
    }


print(batting_summary(6, 10, 25, 75))



    

