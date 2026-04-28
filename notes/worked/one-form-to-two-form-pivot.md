## One-Form to Two-Form Pivot

The difficulty is real. The one-form and the two-form do not seem, at first glance, to be talking about the same kind of thing.

- The `1`-form is action-flavored. It tells us how the action changes when we make one infinitesimal change in one state.
- The `2`-form is ensemble-flavored. It tells us how much state-space room is occupied by a little patch of nearby states.

So why should the second come from the first?

The answer begins with what the boundary term of the varied action is actually measuring. The action is a quantity attached to a whole path. But when we vary it, the boundary term asks a more local question: if we change the state at one time, how does the action respond? That is the moment at which time is, in a sense, factored out. The whole history is still there, but the variation has separated from it the structure of the state at an instant.

From the variation we get

```math
p_i\,\delta q^i.
```

This is not yet an area. It is the action-response to one infinitesimal displacement of the endpoint state. If I nudge the state a little in the `q` direction, this tells me the first-order action-cost of that nudge. So the `1`-form is about one infinitesimal variation of one state.

This is why the boundary term matters so much. The bulk term tells us which paths satisfy the equations of motion. The boundary term tells us what counts as the state at a moment. It says that once we ask for the theory one time-slice at a time, the relevant pair is `q` and `p`.

But Liouville is not about one infinitesimal variation of one state. It is about a cloud of nearby states. A cloud is the smallest thing that can be compressed, stretched, or sheared. One direction is not enough to describe such a cloud. One infinitesimal variation gives only a line of nearby possibilities. A line can be stretched or shrunk, but it does not yet represent local extent in the full space of states.

To get local extent, we need two independent infinitesimal variations. Two such variations span a little parallelogram. That is the first object that can represent an infinitesimal family of nearby states with genuine local size. This is what the `2`-form measures:

```math
dq^i \wedge dp_i.
```

So the `2`-form is not just "one more dimension" added to the `1`-form. It is the first object that can measure the infinitesimal extent of a region of possibilities. That is why it is the right kind of object for Liouville. Liouville is a statement about the preservation of such regions under time evolution.

This gives the bridge:

- the `1`-form tells us how the action responds to one infinitesimal change of state
- the `2`-form tells us the infinitesimal measure of a little patch of nearby states
- the first is path/action flavored
- the second is ensemble/possibility flavored

The surprise is that the second is extracted from the first.

This is why the pivot matters. Lagrangian mechanics appears to speak about one path at a time. But the boundary structure of the action already contains the pairing from which the local geometry of state space can be built. Once that geometry is built, the theory can speak not only about one trajectory, but about a whole cloud of neighboring ones. The jump from paths to ensembles is therefore not a change of subject. It is a development of structure that was already latent in the action.

Put differently:

- the action begins as a statement about a whole history
- the boundary variation tells us what data at one time matter as a state
- that gives the `1`-form pairing `p_i\,\delta q^i`
- from that pairing we build the `2`-form measuring infinitesimal state-space patches
- and those patches are exactly the objects whose preservation Liouville describes

One more distinction helps. The `1`-form is not itself the invariant we care about for Liouville. It is a dynamical-looking object: action-response along one infinitesimal move. The `2`-form is the first intrinsic measure-like object built from that pairing. It is what tells us how much phase-space room a little patch occupies. That is the object whose preservation becomes the infinitesimal content of Liouville.
