def print_domain(name, automata):
    # Generate PDDL domain
    with open(name, 'w') as f:
        print('(define (domain factoring)', file=f)
        preds = []
        for i in range(len(automata)):
            preds.append(f'(state-a{i} ?state-a{i})')
            for token in ['0', '1', 'hashtag']:
                preds.append(f'(transition-consume{token}-a{i} ?old-state-a{i} ?new-state-a{i})')
        preds.sort()
        print('\t(:predicates \n\t\t{})'.format('\n\t\t'.join(preds)), file=f)

        params = []
        for i in range(len(automata)):
            params.append('?old-state-a'+str(i))
            params.append('?new-state-a'+str(i))

        for token in ['0', '1', 'hashtag']:
            print(f'\t(:action consume-{token}', file=f)
            print('\t:parameters ({})'.format(' '.join(params)), file=f)

            precond = []
            for i in range(len(automata)):
                precond.append(f'(state-a{i} ?old-state-a{i})')
                precond.append(f'(transition-consume{token}-a{i} ?old-state-a{i} ?new-state-a{i})')
            precond.sort()
            print('\t:precondition (and \n\t\t{})'.format('\n\t\t'.join(precond)), file=f)

            effs = []
            for i in range(len(automata)):
                effs.append(f'(not (state-a{i} ?old-state-a{i}))')
                effs.append(f'(state-a{i} ?new-state-a{i})')
            effs.sort()
            print('\t:effect (and \n\t\t{})'.format('\n\t\t'.join(effs)), file=f)

            print('\t)', file=f)
        print(')', file=f)

def get_state_name(idx, node):
    if isinstance(node, tuple):
        node_name = '-'.join(str(x) for x in node)
    else:
        node_name = str(node)
    return f"s-a{idx}-{node_name}"


def print_problem(name, automata):
    # Generate PDDL problem
    with open(name, 'w') as f:
        print('(define (problem factoring-1)', file=f)
        print('\t(:domain  factoring)', file=f)

        objects = []
        for automaton_idx, a in enumerate(automata):
            for node in a.graph.keys():
                objects.append(get_state_name(automaton_idx, node))
        objects.sort()
        print('\t(:objects \n\t\t{})'.format('\n\t\t'.join(objects)), file=f)

        init = []
        for automaton_idx, a in enumerate(automata):
            init.append(f"(state-a{automaton_idx} s-a{automaton_idx}-{a.get_initial_state_str()})")
            for key, adj_list in a.graph.items():
                current_node = get_state_name(automaton_idx, key)
                for edge in adj_list:
                    node = edge[0]
                    token = edge[1]
                    next_node = get_state_name(automaton_idx, node)
                    init.append(f"(transition-consume{token}-a{automaton_idx} {current_node} {next_node})")
        init.sort()
        print('\t(:init \n\t\t{})'.format('\n\t\t'.join(init)), file=f)

        goal = []
        for automaton_idx, a in enumerate(automata):
            goal.append(f"(state-a{automaton_idx} s-a{automaton_idx}-T)")
        print('\t(:goal (and \n\t\t{}))'.format('\n\t\t'.join(goal)), file=f)
        print(')', file=f)
