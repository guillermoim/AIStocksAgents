from src import Strategy as st
import random as rd


def __init__():
    pass


def one_point_crossover(s1, s2):
    """
    This method implements the (one-point) crossover method as explained in the paper. The point is fixed so the strategies
    combine the weights with the rest of the parameters.

    Args:
        s1: Parent strategy one.
        s2: Parent strategy two.

    Returns: Two newly bred strategies from the parent strategies.

    """

    s1_params = s1.get_param_list()
    s2_params = s2.get_param_list()

    index = 3

    ls1 = list(s1_params[:index] + s2_params[index:])
    ls2 = list(s2_params[:index] + s1_params[index:])
    new_s1 = st.create_from_list(ls1)
    new_s2 = st.create_from_list(ls2)

    return new_s1, new_s2


def mutation(s, gm, max_t):

    """
    This method implements the mutation of the strategies. The mutation occurs with a probability given and it affects a
    single randomly chosen parameter at once.

    Args:
        s: Strategy to be mutated.
        gm: Mutation rate.
        max_t: Maximum half-life time to be considered by strategies.

    Returns: The strategy mutated.
    """

    # Select a random index to be mutated.
    random_index = rd.randint(0, len(s.get_param_list())-1)

    # Generate a random float representing if the strategy will be mutated.
    aux = rd.random()

    value = 0

    # If aux is greater than the mutation rate, then mutate.
    if aux <= gm:
        if random_index in (0, 1, 2):
            value = round(rd.uniform(0, 1), 2)
        elif random_index in (3, 4, 5):
            value = rd.choice([-1, 1])
        elif random_index in (6, 7, 8):
            value = rd.randint(1, max_t)
    else:
        value = s.get_param_list()[random_index]

    res = st.copy_strategy(s)
    res.set_param(random_index, value)

    return res


def communication(gp, pool, agent, price):

    """
    This method implements the communication process described in the paper.

    Args:

        gp: Communication pool size.
        pool: Pool of agents.
        agent: Agent protagonist of the communication process.
        price: Price at which the wealth of the agents will be computed.

    Returns: Two straetgies resulting from the communication process.
    """

    # Select id of the agent to exclude him from the population
    agent_id = agent.id

    # Generate population and randomly choose gp indices
    population = list(range(0, agent_id)) + list(range(agent_id+1, len(pool)))
    comm_pool_indices = rd.sample(population, gp)

    # Map indices to agents
    comm_pool = [pool[i] for i in comm_pool_indices]

    # Perform the communication process as described in the article
    counter = 0
    takes_advice = False

    for a in comm_pool:
        if agent.get_wealth(price) < a.get_wealth(price):
            counter += 1
            if counter > gp//2:
                takes_advice = not takes_advice
                break

    a = st.copy_strategy(agent.get_strategies_by_profit(price)[-4])
    b = st.copy_strategy(agent.get_strategies_by_profit(price)[-3])

    if takes_advice:
        (a1, a2) = sorted(comm_pool, key=lambda x: x.get_wealth(price), reverse=True)[0:2]
        a = st.copy_strategy(a1.get_top_strategy(price))
        b = st.copy_strategy(a2.get_top_strategy(price))

    return a, b
