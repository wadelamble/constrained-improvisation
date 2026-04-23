*Quotes*

Symmetry is … the outward sign of inner unity. – M.C. Escher

There is geometry in the humming of the strings. There is music in the spacing of the spheres. – Pythagoras

There is still a difference between something and nothing, but it is purely geometrical and there is nothing behind the geometry. -Martin Gardner

A Love Supreme – John Coltrane

If that’s all there is, then let’s keep dancing – Peggy Lee

# Introduction

There are those among us who are guilty of having an almost mystical awe for physics. When propositions dripping with metaphor like “energy generates time” or “matter represents symmetry” or bespeaking some sorcery like “time slows down” or “a thing is in two places at once” are understood as literal mathematical formulations, with their attendant rigorous definitions, one can feel they are brushing against some monastic secret. Fortunately, such grandiosity is counterbalanced by a creed of humility among physicists that has been enforced by facts nature has revealed. From Galileo to Einstein, breakthroughs have been made by focusing on the observer, asking not the arrogant “what is,” but the humble “what do we see.” With the discovery of quantum mechanics, this humility takes an even more radical turn, seeming to imply that even our categories of “object” and “location” are overstepping the bounds of what we can safely presuppose. This interplay of following mathematical forms wherever they lead while trusting observation as the only criteria of knowledge is the source of physics’ allure and success.

What is a physical system? We might think of two billiard balls bouncing off each other or a fluid circulating. These are different, but we recognize them both as something physics would study. What do they have in common?

1.  Some identifiable material

2.  Some notion of motion, or change

3.  Some pattern of change that persists whether the system is “here” or “there,” “now” or “then.”

One might think we build up a physical theory by starting with the first, “what is there,” adding the second, “how does it move,” and finally arriving at the third, what ensures it maintains consistency from different, valid, perspectives, that is, what are its “symmetries.” But in fact, the way physics is understood by its practitioners today proceeds in the opposite direction. It seeks first to ask what “symmetries” are present, then to ask how to mathematically describe motion in a way that is consistent with those symmetries, and finally, to ask what sorts of objects such a model admits. This is the statistical way of thinking, in which assertions of knowledge are made in the form of distributions.

Beyond symmetry as a starting point, physics is built from a handful of additional principles.

- Local Causality. There is a causal structure to physical reality that is reflected in the structure of space and time, or simply spacetime. That is, an event “here” cannot impact an event “there” faster than the time it takes light to travel that distance. This causal structure is, it turns out, “weak,” in the sense that, while it does preclude instantaneous communication, it does not preclude the instantaneous enforcement of correlations over spatial separation.

- Probability. At sufficiently small scales it becomes noticeable that measurements are members of a probability distribution that is given by a function that evolves as a wave packet over that observable.

- The Principle of Least Action. A system follows the straightest path it can in the geometry that reflects its symmetry and curvature. For a free particle, this means it goes in a straight line, but if a system lives in curved geometry, much as the shortest flight path on earth is a geodesic, “straightest” is determined by the details of the curvature. The space that is curved is spacetime itself with additional “internal” symmetries superposed onto it. Action I the invariant quantity that all observers – no matter their orientation – agree on that measures this path length. Following such curved paths manifests as “force.”

These may be the almost self-evident truths from which our understanding of physics derives, but within these constraints nature makes some choices on its own – that we only know through experiment – in the form of physical constants. These include:

- h = 6.626 070 15 × 10⁻³⁴ J⋅s. Planks constant. The scale (in terms of action) at which matter and energy are innately distributed over quantized values.

- c = 2.997 924 58 × 10⁸ m⋅s⁻¹. Speed of light. The upper bound of velocity inherent in the structure of spacetime.

- G = 6.674 30 × 10⁻¹¹ m³⋅kg⁻¹⋅s⁻². Universal gravitational constant. The scale factor relating energy distribution to spacetime curvature.

- All the masses and other intrinsic properties like spin and charge of fundamental “particles.”

It is astounding that our physical theories specify a set of just a few knobs nature can dial to create our world and that we can then measure those values through experiment.

There is one more element in physical theories that is neither “self-evident first principle” nor “knobs nature dials.” When we construct the space in which a system evolves and write down its *action*, we have a choice of “rulers” that would all be mathematically consistent. For instance, we could measure velocity separation using $`v^{2}`$or $`v^{4}`$. In practice, the simplest one – the one involving only the lowest powers of the dynamical variables like positions and their rates of change – almost always suffices, because at the energy scales we can reach, the effects of higher powers are negligible. This arrangement is neither a principle, nor a fact of nature, but an approximation that works in any regime accessible to experiment. As much as physics seems to have a pure quality that it uses math to “tell the story,” it is in this respect, in the “choice of the representative function” that physics must confess, it, too, is but a model.

Our principles – of symmetry, causality, unitarity, and least action – leads to a solution, a story of material reality that abides these principles, and that is a story of waves, of harmonics and pulses, of, in a word, of music, that is, as best we can tell, the way nature is.

*Readers Notes*

It is my hope that some curious reader without any particular background in science, but with a desire to dig deeper than the inherently limited metaphors of pop science can afford, will enjoy reading this paper. I also know, as I am one, that there is a contingent of physics fans that enjoy conceptual rigor and are served by various authors, podcasters and YouTubers. I would be delighted to have a reader among this contingent. However, the audience I most hope to reach is young people who may be considering a career in Physics. Physics curriculum is aimed at teaching people to “do physics” as much as to “learn physics,” and, in serving these dual purposes, has, I believe, a tragic flaw. The aspects of physics that make it a crowning achievement of human intellect are both obscured in the minutiae of problem solving and delayed until graduate school. If I could help one undergraduate student enjoy their curriculum more by having a context to put it in, I will have reached the goal of writing this paper.

If one does read the entirety of what follows, they may feel cheated. There are few equations of motion and no solutions to actual physical systems. We do discuss the electromagnetic force law. The reason that we only get this far is that we are focusing on the *fundamental* picture beneath these laws.

I have not attempted to avoid math because some ideas are simply more effectively communicated in mathematical notation than in prose. There is no multi-step algebra. Math expressions are instead used as the most impactful way to summarize discussion. I have tried to explain any notation as I use it.

We will begin by learning the language of symmetry, introduce Special Relativity and the structure of spacetime using this language, discuss how spacetime symmetry can be represented by waves, associate waves in quantum mechanics with encoding measurements of essentially probabilistic phenomena, discuss how the physical path is what is left after cancelling out at the probabilistic level, learn about General Relativity and how curvature leads to force, build on that by discussing curvature in more complex geometries in which additional symmetries are layered on spacetime and how such curvature is mirrored by dynamic flows, and finally discuss how quantum field theory, and quantum electrodynamics specifically, explains electrons, photons, particle interactions, and the electromagnetic force. The reader with a physics background will notice many omissions. First, as mentioned above, we only cover fundamental concepts, excluding most notably systems of many particles and, with that, any discussion of the properties of matter that arise from statistics or thermodynamics. Second, we stop at QED. Weak and strong forces are not mentioned. Third, and perhaps most contentiously, we do not cover classical “Newtonian” or “Hamiltonian” mechanics or classical electromagnetic theory. Hamiltonian mechanics contains ideas about symmetry that we implicitly pick up, but it treats time in isolation rather than as a unified spacetime dimension. Grounding our story in spacetime up front and sticking with that hopefully yields conceptual clarity and economy. Taking this approach requires only “Lagrangian” mechanics. Classical electromagnetic theory contains the seeds of special relativity, gauge theory, and wave representations. But we can arrive at it through the conceptual front door of QED rather than trying to understand it on its own without this richer theoretic framework.

# 

# Geometry and Physics

Imagine, if you will, Plato’s students huddled around the master, drawing circles in the sand, meditating on the meaning of $`\pi`$. They know that if the diameter of a circle is 1 the circumference is $`\pi`$. They measure different circles and tabulate the radii and circumferences. They *could* treat this table as purely empirical set of results, but being the good geometers they are, they think of it differently. They appreciate each drawing in the sand as a material instance of the geometric form. They can “convert” between the geometric form and their measured results with some scale factor, or constant of proportionality. Let’s put a wrinkle in our story. Let’s say in nature, circles only ever come in one size, 12 inches in diameter. Plato’s students will then say “nature’s circles are geometry’s unit circles time 12 inches.” Notice the scale factor has a value and units, inches in this case.\
\
This, really, is the project of physics. We theorize a geometry with various objects in it – surfaces, waves, loops, curvature – and, thought scale factors, map that onto the world we can measure. Plato, famously, wanted to say geometry was real and its instantiation in nature was but a trivial shadow. Take that or leave it. But what is undeniable is that when a physical theory is good, when it explains more and more, it progresses to a great degree by making inferences *in* the geometry, just like high school geometry proofs. At the very least, we should appreciate the importance of taking the geometry, the form, the structure in how we make sense of our world.

# Symmetry

When we say “symmetry,” we really mean symmetry, like, you know, triangles, snowflakes, etc. The math for the symmetry of continuous spaces with coordinates is an outgrowth of the math for the symmetry of shapes. So let’s take a bit of time to learn about the mathematical treatment of symmetry

Before we dive into symmetry as such, let’s clarify this odd idea that “picking up your experiment and move it over there” constitutes a “symmetry.” It’s not obvious what this means. Consider the line simply as a shape and assume it has infinite length. Can you see the difference when we move it left or right? No. Thus the shape itself is symmetric with respect to “translations.”

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image1.png)

Figure 1 - The symmetry of a line

The “sameness” of the physics when our experiment is translated along a given dimension is treated in the same way as the sameness of the line shape. The symmetric “action” is translation and the shape of a line and physical behavior “realize” translational symmetry.

## Discreet symmetries

When we work through the concepts of particle classification in quantum mechanics we will throw around terms that can seem abstract or opaque, but which we can build up to from working through simple examples of symmetry. Let’s start with examples of shapes with “discreet” symmetries. The humble equilateral triangle is a suitable example. We can see at a glance that it has symmetries, for example, rotating by 120 degrees. We can also see that the characteristic symmetries of triangles are present in other “triangly” objects.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image2.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image3.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image4.png)

Figure 2 - Triangly things

There is a menagerie of shapes that have the same symmetries, but what are the symmetries, how do we define them without drawing more shapes? Let’s try. If you rotate the triangle a little bit, it doesn’t look that same – that’s not a symmetry.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image5.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image6.png)

Figure 3 - Rotating a little bit is not a symmetry

But what if we rotate it by 120 degrees? Or 240 degrees? Those do make the shape look the same. And what if we flip along an axis going from one vertex and bisecting the opposite side. That is also a symmetry.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image7.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image8.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image9.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image10.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image11.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image12.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image13.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image14.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image15.png)

Figure 4 - Rotation and Flip symmetries

# 

There are six total symmetries: three rotations and three flips. These actions form a “**symmetry group**.” We should pause here to stress something. The symmetry group is not the group of triangly things, but the group of actions that preserve the symmetry of the triangly things. For what it’s worth this particular group is called $`D_{3}`$, the dihedral group of order six. Whoa.

Whenever we have a symmetry, we must have some “**invariant**,” some way of defining what we mean by “is the same.” For triangles, one way to express the invariance is that vertices are always at the same location. This may seem pedantic, but it becomes all important when we work in a coordinate space, where the invariant becomes a number whose value classifies objects.

We can build up the symmetry preserving actions of $`D_{3}`$ from two actions. Rotation by 120 degrees and flipping along one axis. These building block actions are “**generators**.”

At this point, we need to take a bit of a conceptual leap. We can map the objects groups act on to vectors in a vector space and the group actions to matrices that transform the vectors. Once we do this, we can “do linear algebra” on symmetry groups, and that, in sense, is the plot setup for modern physics -- physical behavior is the symmetric thing, and the map onto linear algebra allows unpacking the story in numbers. So, let’s try it with the triangle. We can represent a triangle as a vector as follows:

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image16.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image17.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image18.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image19.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image20.png)

Figure 5 - Triangle A,B,C -\> Vector \[A, B, C\]

Now let’s say we want to take vertex A to vertex B, leaving C alone. We do that multiplying the “triangle-vector” with the “rotation” matrix:

``` math
\begin{bmatrix}
0 & 1 & 0 \\
1 & 0 & 0 \\
0 & 0 & 1
\end{bmatrix}
```

We call a particular linear algebra representation of the group, well, a “**representation**.” It’s important to note that different vector representations may correspond to different objects. For example, some more complex shape might have as long as it realizes the symmetry group. For example, a shape with $`D_{3}`$ symmetry that has some more complex shape may require a higher dimensional vector to represent it, but that vector space is still a representation of $`D_{3}.`$

What if we instead put our triangle in a 2d plane and rotate it?

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image21.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image22.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image23.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image24.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image25.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image26.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image27.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image12.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image28.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image29.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image30.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image31.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image32.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image33.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image34.png)

# 

Figure 6 - Rotate a Triangle in 2d space keeping track of the vector corresponding to one vertex

Our triangle is now represented by the single vector $`\left\lbrack \begin{array}{r}
0 \\
1
\end{array} \right\rbrack`$ (the other vertices are implied) and we can rotate it 120 degrees with the matrix $`\begin{bmatrix}
\cos(120) & - \sin(120) \\
\sin(120) & \cos(120)
\end{bmatrix}`$. We could construct matrices in this space that also represent flips. This representation is a subspace of our previous representation realizes the same symmetry actions. When we have such a space that doesn’t have any other lower dimensional subspace that represents the group, we call this an “**irreducible representation**,” or “**irrep**.”

These concepts – group actions, invariants, generators, representations, and irreducible representations – in the context of triangles may seem out of left field, but they turn out to be the building blocks of the theory of Quantum Mechanics.

Many of the concepts from symmetry in physics require us to deal not with “discreet” symmetries like triangles exhibit, but with continuous symmetries such as circles. Recall rotating a triangle a little bit did not preserve the symmetry. On the other hand, rotating a circle by any amount is a symmetry-preserving action.

# ![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image35.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image36.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image37.png)

# ![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image38.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image39.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image40.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image41.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image42.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image43.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image44.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image45.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image46.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image47.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image48.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image49.png)

Figure 7 - Any amount of rotation preserves the symmetry of a circle

The circle has an infinite number of group actions corresponding to rotation by any angle. ~~Much as the calculus student who loses herself in abstraction can always fall back to discreet differences and sums to regain her footing, so we can fall back to triangles to demystify continuous symmetries.~~ The circle group is called, for what it’s worth, SO(1). This group’s invariant is actually easier to define than the triangle’s. It is simply the length of any vector from the origin, that is $`\sqrt{x^{2} + y^{2}} = const`$. What is the generator of this group’s actions, of rotations? It is an infinitesimal rotation. Very significantly, a general principle of geometry is that everything is flat when you zoom in far enough. Since “infinitesimal” is fully zoomed in, such a rotation is “flat,” that is, it is a tangent vector.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image50.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image51.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image52.png)

Figure 8 - Tangent vectors generate rotations

And what is the tangent to a circle? Let’s work it out. We can label any point on the circle as $`\left\lbrack \begin{array}{r}
\cos\theta \\
\sin\theta
\end{array} \right\rbrack`$. As every calculus student learns, the tangent vector of any function is the derivative of the function. Thus the tangent is $`\left\lbrack \begin{array}{r}
\sin\theta \\
\cos\theta
\end{array} \right\rbrack`$.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image53.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image54.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image55.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image56.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image57.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image58.png)

Figure 9 - labelling a point on the circle and the tangent vector with sin and cos functions.

So what is the generator of rotations? Thinking back to the triangle, the generator was the action of rotating 120 degrees. Here our action is a function that labels the circle at every point. What performs that action? It is:

``` math
\frac{\mathbb{d}}{\mathbb{d}\theta}
```

This funny looking thing is an “**operator**.” Since a function has values at every point, it is equivalent to an infinite dimensional vector and an operator is equivalent to an infinite-dimensional matrix that maps one infinite dimensional vector to a new one.

### Momentum as Generator of Translations

Physicists are fond of saying that momentum “generates” translations and, poetically, energy generates time, a phrase worth meditating on. We can now see what this means in terms of symmetry.

As we discussed above, translation is a symmetry. In notation we would define translation as an operation that takes a vector and shifts it. In notation:

``` math
x \mapsto x + a
```

If this is a symmetry, it must fulfill the requirements of symmetry group

1.  If we translate by a, then by b, translating by (a + b) is still a translation

2.  If we translate by a + b and then by c, that is the same as translating by a, then b + c.

These relations are super obvious for translations. The point in saying them out loud is that we have *not* yet said how to **represent** translational symmetry, that is to express it in some linear algebra (vectors and matrices acting on them) space. The most obvious representation is for a single point in a single dimension:

``` math
T(a) = x + a
```

Here T(a) is the “translation operator.”

This is fine, but what if we have a system with multiple objects at different coordinates and we want to “pick up and move” the system. Then we need a representation that can carry this structure. We can do this with vectors and matrices in two dimensions:

``` math
\begin{bmatrix}
1 & 0 & a \\
0 & 1 & a \\
0 & 0 & 1
\end{bmatrix}\left\lbrack \begin{array}{r}
x_{1} \\
x_{2} \\
1
\end{array} \right\rbrack
```

But what if we have 3 objects in our system? Or what if we have a whole field with infinite points, like waves on a pond? To fully represent our physical system, we need to represent the symmetry in function space:

$`\lbrack M\rbrack\left\lbrack \begin{array}{r}
x_{1} \\
x_{2} \\
. \\
. \\
. \\
x_{\infty}
\end{array} \right\rbrack`$

Or, in its more normal form:

$`\widehat{O}\left( f(x) \right)`$ where $`\widehat{O}`$ means some operator that acts on $`f(x)`$, such as d/dx:

``` math
\frac{\mathbb{d}\left( f(x) \right)}{\mathbb{d}x}
```

Recall that the infinite dimensional vector form of the function means the value of $`f(x)`$ at every $`x`$.

In this representation, we can think of the symmetry action as shifting a function.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image59.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image60.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image61.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image62.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image63.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image64.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image65.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image66.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image67.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image68.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image69.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image70.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image71.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image72.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image73.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image74.png)

Figure 10 - Shifting a function by an amout a

Another way to say this is that if we have translational symmetry in a dimension and some function on the dimension, if we move from one location to another, we can leave the function the same and just slide the coordinate system.

We know that continuous symmetries have generators that act to produce an infinitesimal shift. Let’s try to find that generator for translations. Things get a bit heavy mathematically here. We know from calculus that we can Taylor expand any function as:

$`f(x + a) = f(x) + a\frac{\mathbb{d}\left( f(x) \right)}{\mathbb{d}x} + \frac{a^{2}\mathbb{d}^{2}\left( f(x) \right)}{2!} + \ldots`$ = $`\mathbb{e}^{a\left( \frac{\mathbb{d}}{\mathbb{d}x} \right)}`$.

(It would take time to really motivate the idea of a Taylor expansion, but very briefly, it is saying that if you know the value of a function at one point and all the derivatives of the function – how fast it changes, how fast its change changes, and so on – you can – quite astonishingly – find the value of the function at any other point.) In any case, we have now found the translation operator:\
``` math
T(a) = \mathbb{e}^{a\left( \frac{d}{ax} \right)}
```

Doing a bit more calculus magic we can say that if $`a`$ is an infinitesimally small shift, we only need the first two terms of the expansion as the remaining terms get small faster than $`a`$ does. We then have just:

$`f(x + a) = f(x) + a\frac{\mathbb{d}\left( f(x) \right)}{\mathbb{d}x}`$ (for infinitesimal values of a)

We then have our generator of translations:

$`\widehat{a}f(x) = a\frac{\mathbb{d}\left( f(x) \right)}{\mathbb{d}x} \Rightarrow \widehat{a} = a\frac{\mathbb{d}}{\mathbb{d}x}`$ where $`\widehat{a}`$ is the translation generator.

We are free to use $`a`$ to be what we want. Once we choose $`a`$, we can find the **eigenfunctions** of the operator. An eigenfunction is a function that only changes by a scale factor when the operator acts on it. This is analogous to the way axis is an eigenvector of rotation – no matter how much you rotate, the axis stays the same. No matter how many times you differentiate, the function maintains its shape. The beauty of finding an eigenfunction is that when you do, you have an “axis” or a “basis” (like x, y, z is a basis for normal 3d space) for space of generators of translations. The eigenfunction will be of the form:

``` math
f(x) = \mathbb{e}^{ax}
```

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image75.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image76.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image77.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image78.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image79.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image80.png)If we choose $`a`$ to be real, our eigenfunctions grow without bound. These can encode the symmetry, that is, they can reflect the symmetry in a predictable way, but they do not retain their shape over $`x`$, which we can plainly see:

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image81.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image82.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image83.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image84.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image85.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image86.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image87.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image88.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image89.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image90.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image91.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image92.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image93.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image94.png)

Figure 11 - plots of plane waves and real exponentials - plane waves are symmetric

Functions of the form $`\mathbb{e}^{\mathbb{i}kx}`$ are simply **complex** **plane waves (**their real components are simply sinusoidal waves.) Keeping in mind that our plane wave extends to infinity in both directions, we can see that shifting it left or right has no impact on its shape. This is the essence of saying it represents translational symmetry. Algebraically:

``` math
{\left( T\overline{}a \right) = \mathbb{e}^{\mathbb{i}ka}\mathbb{e}^{\mathbb{i}kx}
}
```
And we see that $`\mathbb{e}^{\mathbb{i}ka}`$ is precisely just a phase factor.

We can also see that because a complex wave lies on a “cylinder” of constant radius, changing the phase does not change the length. Thus, the amplitude at any point is unaffected by translation. When we talk about quantum mechanics and “bodies” being probability distributions, probability will be associated with amplitude, and the fact that the translation operator does not affect amplitude will likewise imply it does not impact probability, which provides that property that symmetry translation (of particular interest when the symmetry is time) preserve total probably (of 1). This probability preserving property is called “Unitarity,” from the idea that the infinite dimensional vector corresponding to a plan wave always lies on the “unit sphere.” If the term Unitarity seems to invoke something more poetic, like oneness or integrity, I suppose that is by design – it is a deeply fundamental property of quantum story of reality. Unitarity tells us more than just that the amplitude of a plane wave is unaffected by translation. To understand it fully, we need to understand how it acts on a superposition of plane wave. A single plane wave is just one vector in a vector space of wavey things. Because plane waves are eigenfunctions, they form a basis for an infinite dimensional space of wavey things, or wave packets, if you like. Any superposition of plane waves is a vector in this space, and these vectors all lie on a unit sphere. A unitary operator is a rotation of this sphere. Thus it preserves the amplitude of any wave packet. These properties are wrapped up in the single property that unitary operator preserve the dot product between the vectors they act on:

``` math
\left\langle Uf(x) \cdot Ug(x) \right\rangle = \left\langle f(x) \cdot g(x) \right\rangle
```

What are the “wavy things” that live in this space? They are most any functions that “look like a wave packet” and don’t blow up any where. Below are visual examples.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image95.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image96.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image97.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image65.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image98.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image99.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image100.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image101.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image102.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image103.png)

Figure 12 - Examples of functions that can be composed from plane waves

This composition of wave packets in a basis of plane waves along with the unitarity of the translation operator is the basis of the famous Fourier Analysis that allows transforming between position and momentum representations, that is between wave packets and their decomposition in terms of pure plane waves. This is at the heart of many topics in engineering and science from the synthesizer design to the uncertainty principle in Quantum Mechanics.

It's really worth stepping back and appreciating this bit of math. We’ve combined complex numbers, calculus, exponential functions, curvature and flatness to show how observable, instinctive symmetry leads to dynamical, conserved physical quantities, all with no reference to any particular coordinate system.

#### Momentum

The equation:

$`\widehat{a}\ \left( f(x) \right) = a\frac{\mathbb{d}\left( f(x) \right)}{\mathbb{d}x}`$

is valid for any value any value of $`x`$. Thus, when we act with it, we move to a new value,

``` math
x \mapsto x + a
```

the equation still holds. Therefore, the eigenvalue $`a`$ does not change as we move along a symmetry. Thus, we associate the role of $`\widehat{a}`$ as the generator spatial translation with $`a`$ being a conserved when there is spatial symmetry. This is the essence of momentum, replacing our generic $`a`$ with the normal symbol for momentum $`p`$, we have

$`\widehat{p} = \mathbb{i}\frac{\mathbb{d}}{\mathbb{d}x}`$ =\> $`\widehat{p}\left( f(x) \right) = pf(x)`$

In a system with more than one body in a symmetric space, interactions between bodies may change the total velocity vector, but they preserve the total (center of mass) momentum vector. When we say in high school physics that two billiard balls colliding conserves momentum, we are saying that the eigenvalue of the translation operator is conserved. The same relationship holds for any symmetry we can find in a system. Interestingly, we have defined momentum with no mention of mass, and yet, we learn very early in physics that:

``` math
p = mv
```

Assuming $`v`$ is a fundamental (non-derivable) as the expression of “motion” itself, does this mean that mass is not fundamental? That it somehow arises from symmetry. Yes! That is exactly the case, but we will need to wait until discussion spacetime and Relativity to show it.

#### Commutation

When you move around the world, you compose different “degrees of freedom of symmetry,” such as up/down, left/right, spin around. Where you end up depends on the order in which you combined the motions. The simplest example is that rotations don’t commute, that is, the order of motions does matter. Specifically:

``` math
\left\lbrack L_{x_{i}}L_{y} \right\rbrack = L_{z}
```

This says if you compare rotating in x then y to rotating if y then x, the difference is a rotation in z, which you can convince yourself of by rotating a book.

Mathematically, we apply symmetries in order as follows:

``` math
f(\alpha) \circ g(\alpha) = \exp(F + G)
```

When we compute $`\exp(F + G)`$ using the Taylor expansion definition, if there are commutation relations, $`\exp(F + G){\ ! = \ exp}(F)\exp(G)`$the other defining property of exponentiation. To make the property hold, we correct the exponent using commutators.

``` math
\exp{(A)\exp(B)} = \exp\left( A + B + 2\lbrack A,B\rbrack + \ldots \right)
```

The commutator is thought of as an expression of the overall shape, or **curvature**, of the symmetry. We measure the commutator by the difference given by reversed order of application:

``` math
\lbrack F,G\rbrack = FG - GF
```

And we think of the commutator as “the actual difference in order of operation, shrunk to tiny, flat steps.”

The commutator comes up again and again in Quantum Mechanics which is framed in terms of symmetry. It can be confusing that some explanations begin with the commutator. But once you realize that the commutator and the generators themselves come from the same place, the “shape” of the symmetry, you see that it gives you an alternate mathematical formulation of the symmetry. One can find operators in terms of commutators using the Lie Algebra equations.

$`\left\lbrack A_{i},A_{j} \right\rbrack = \Sigma_{k}c_{\mathbb{i}j}^{k}A_{k}`$\
\
When the symmetry is represented and given a basis, these equations amount to matrix equations that define the symmetry from a linear algebra perspective.

Random formula:

``` math
g(\alpha) = \exp\left( \alpha^{a}G_{a} \right)
```

*To move around in a symmetric world, you compose group actions of the different symmetries:*

*What is this saying? It says, on the left hand side, “to move around in a world with our symmetries by an amount alpha,” you, on the right hand side, “exponentiate an alpha’s worth contribution from each symmetry’s generator.”*

**Common fixes to your draft**

- Use $`\left\lbrack L_{x},L_{y} \right\rbrack = L_{z}`$(with possible $`i`$factors), not $`\left\lbrack L_{x_{i}}L_{y} \right\rbrack = L_{z}`$.

- The BCH leading term is $`½\ \lbrack A,B\rbrack`$, **not** $`2\lbrack A,B\rbrack`$.

- Do not write $`f(\alpha) \circ g(\alpha) = \exp(F + G)`$. Composition of exponentials is governed by BCH, not by the naive law of exponents unless $`\lbrack F,G\rbrack = 0`$.

#### From Symmetry to Geometry

We live in a space that we feel in our bones. Up, down, left, right. Knowing this space, we immediately know what symmetries to expect, in the sense that things behave the same under symmetric transformations. (Pick up your experiment and take it over there – nothing changes. Put it on a train – nothing changes.) If one were to try to pin us down on how we define this space we intuitively know so well, what would we say? Well, one answer, maybe the only answer, is precisely to move our experiment around to establish our space’s symmetries. And that becomes the definition of our space. It may be the sort of space where things move freely past each other, where speeds build to infinity, or the kind where things fall toward each other and speeds meet infinite resistance approaching some speed, that is all to be figured out. As a bonus from defining space this way, we get a recipe for developing a coordinate system that maps symmetry transformations. These transforms allow us to make predictions, which validate our original assertions about the symmetry. So one can guess at the symmetries, work out their coordinate transformations, and test whether the guess of the symmetries was correct. And there you have the project of mathematical fundamental particle physics. The space in which the symmetry resides is not less real than the symmetry in this view, however, epistemologically, it is the sameness of the experiment that defines the geometry of the space and is the starting point for a mathematical description of motion in that space.

Let’s try to get an overview of this mathematical procedure for going from symmetry to geometry. First, let’s define the terms. We’ve already defined symmetry in two ways – the ways you can arrange a shape that leave it in some way invariant and, in physics, the ways you can move a physical system, like a billiard table, and leave it invariant in terms of physical behavior. Geometry is the rules governing angles and distances. Everyone knows the angles of a triangle add up to 180 degrees. But on a sphere that’s not true, they add to more than 180 degrees, and on a hyperboloid, they add to less than 180 degrees.

<figure>
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image104.png" style="width:3.26044in;height:1.02084in" alt="A green triangle with black text AI-generated content may be incorrect." />
<figcaption><p>Figure 13 - Sum of Triangle Interior Angles with Curvature</p></figcaption>
</figure>

Likewise, distances depend on a space’s symmetries. This may seem

But, you may object, a sphere is just and “object” sitting in a “space,” where the angles in a triangle add to 180 degrees. That is true, and it leads to one of the fundamental things that “following the math” tells us about the world – spaces can have curvature *intrinsically* without being embedded in another space. This is hard to wrap one’s head around because we are so very accustomed to flat space. How, you might ask, would you know you lived in curved in space without “looking down on it” from some higher dimensional space, as we can see the earth from space. Math offers a rigorous answer to this question as follows. If you carry an arrow and hold it straight as we walk. Once we complete a loop the arrow will point in a different direction than it did when we began. How different it is tells us the space’s curvature.

<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image105.png" style="width:3.36653in;height:1.93252in" alt="A screen shot of a globe AI-generated content may be incorrect." />\
\
Figure 14 - Measuring Curvature with Parallel Transport

This may be a bit difficult to visualize, but the important point is to convince yourself that if, say, a flat insect’s entire universe were confined to the surface of the earth, it could still tell it lived on curved space, even as each small patch seemed flat.

Our job is to take the symmetries that we discover through experiment or intuition, discover the “shape” that carries that symmetry, and then write down the geometry for that a world that exists within that shape. Since physical symmetries are continuous – we can move our experiments by any amount, we want to apply the basic idea of calculus to our space. We want to say, if we parallel transport along a tiny loop and probe the shape of our space, because the space is symmetric, we can act with those tiny motions over and over and get a predictable result, which we express through exponentiation. We’ve seen this above. The equations that encode the parallel transport behavior around a tiny loop are just the commutation relationships:

``` math
\left\lbrack A_{i},A_{j} \right\rbrack = \Sigma_{k}c_{\mathbb{i}j}^{k}A_{k}
```

Each A (i, j, k) is a step in a given direction corresponding to the dimension of the symmetry group. For example, there are 3 generators for rotating a sphere.

#### Symmetry to Stage

Our first step is, given our symmetries, to construct the stage, or base space, on which these symmetries act. We do this by “dividing” the full symmetry space by the symmetries that leave an origin fixed – namely, rotations. This “quotient space” establishes the notion of a space of “points” that one can move around in via translations. In notation:

``` math
M = \frac{G}{H}
```

where $`M`$ is some physical stage, G is the full symmetry group, and H is the “stabilizer group” that leaves an origin unchanged. This gives us what mathematicians call a “coset,” a set of points in space. This shrinks all the rotation and boost symmetries down to a point, that is, it says to think of the rotation symmetries as a “person turning” rather than the “world turning.” And then you can package all rotations into an “observer,” leaving only the translation operators. The way that the translation operators change when an observer rotates (boost are rotations too) spells out a “incompressible fluid flow.” For example, if, in this fluid, when you turned, you got swept away quickly, that would imply a symmetry in which physical behavior would dictate that our reading of time and space coordinates gets “swept away,” and with it our reading of momentum. Spoiler alert, this is exactly the situation in Relativity’s understanding of the spacetime. Under this “fluid flow,” we can identify the thing that stays the same when we rotate (and translate, which we think of as a transformed copy of any given observer) in terms of the separation of two points under the flow. How to measure the invariant separation is the idea of dot product. It needn’t always be a length as we think of it, it only needs to be reflective of the fluid flow corresponding to the symmetry. Once we have this, the dot product, or more generally inner product, we can define a coordinate system and a way to measure its curvature. At that point, we are ready to “do physics” with rulers and clocks.

How does one go from an understanding of a system’s symmetries to a testable, quantitative formulation of physical behavior? At its most basic level, that quantification is the path an object follows:

``` math
x(t)
```

But who is saying this path is? If I’m looking at a star 50 trillion miles away from me and turn half a turn to put the start behind me, it didn’t suddenly travel 100 trillion miles, but $`x(t)`$ did change that much. In order to write $`x(t)`$ we must specify an observer and specify that observers orientation. Once we have done so, we have a *frame of reference.* Different frames of reference are a reflection of the physical symmetry, that is, the fact that all frames of reference agree on physical behavior is what we mean by symmetry. Not all observers will agree on physical behavior. If one were to try to play pool on a train car oscillating back and forth, the behavior of pool balls would be unrecognizable. The frames of reference that we have in mind are precisely those in which physical behavior does not change. Now, identifying an observer and writing $`x(t)`$ for that observer is just a starting point. In order to capture “that behavior all frames agree on” we must have a way to *transform* “my” $`x(t)`$ to “your” $`x(t).`$ That is, if I’m “here, facing north, going 10 mph” and you you are “there, facing east, going 20 mph” for every $`x`$ from my perspective, I must have a way to that to an $`x`$ from your perspective. And since that transformation must be done such that the physical behavior stays the same, we can ascertain that the transformation must, at the very least, leave *something* the same. This is just the idea that a symmetry must have some invariant, but now, that invariant must be expressible in coordinates, in terms of $`x`$. What would do for the invariant. Well, let’s give ourselves two rigid rods. When we rotate, we plainly see that the rods lengths stay the same and the angle between them stays the same:

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image106.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image107.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image108.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image109.png)

Figure 15 - Lengths and Angles don't change under rotation

Now, how can we capture this in terms of coordinates? The tried-and-true answer is the dot product. We take the vertex of our rods, place that at the origin, treating each rod as a vector, and then calculate, for example in two dimensions:

``` math
< v1,\ v2 > \  = \ (ab)\left( \begin{array}{r}
c \\
d
\end{array} \right) = ac + bd
```

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image110.png)Visually, this is calculating the projection of one vector on the other, scaled by their lengths:

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image110.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image111.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image112.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image113.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image110.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image114.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image115.png)

Figure 16 - Visualization of Dot Product

Note that a vector dotted with itself just gives its length, thus for a single vector, the dot product serves to encode the invariance of its length. Now, we could have written this differently, as:\
``` math
{\left\langle v_{1},v_{2} \right\rangle = (ab)\begin{pmatrix}
1 & 0 \\
0 & 1
\end{pmatrix}\left( \begin{array}{r}
c \\
d
\end{array} \right)
}{
Here\ the\ identity\ matrix\ is\ doing\ nothing.\ But\ what\ if\ it\ were\ not\ the\ identity\ matrix?\ What\ meaning\ would\ that\ have?\ \ }
```
We have to allow our imaginations to roam wild a bit here. First, we have to make the association that geometry ***is*** the world we live in, not some structure known a priori that we map our world onto. With that in mind, can imagine we live in a world where, if we are holding a stick and rotate, the stick grows, that is, $`\left\langle v_{1},v_{2} \right\rangle`$ gets larger. We can further imagine it grows to infinity as we turn, and we can never, ever turn all the way around – some unseen resistance just builds as our stick approaches infinity. Let’s say this is the measuring stick we use to measure physical behavior. And while the stick grows, it nonetheless yields a consistent picture of physical behavior in which billiard balls do billiard ball like things. Well, clearly we didn’t choose $`\left\langle v_{1},v_{2} \right\rangle`$ correctly, for it is not invariant. But we can fix this by changing our identity matrix above to a different *metric*. In fact, there is a metric matrix that works perfectly for the symmetry we just described in words:

$`\left\langle v_{1},v_{2} \right\rangle = (a,b)\begin{pmatrix}
 - 1 & 0 \\
0 & 1
\end{pmatrix}\left( \begin{array}{r}
c \\
d
\end{array} \right)`$\
\
This is the metric (- +) for hyperbolic symmetry. Imagine sliding a vector along a hyperbola. Its length grows (from our accustomed perspective). But we could define the invariant inner product this way, and then say, “when you rotate and measure some physical system, you have to transform your measuring stick this way in order for the physical behavior to look the same.” Here we worked from the metric to the symmetry, but we can go the opposite direction, and, with careful consideration, work from the symmetry to the metric.

# Relativity

## Relativity from Symmetry

Let’s follow this procedure to discover the geometry of space and time that we inhabit. As a bonus, we’ll be able to show how the “wrong” Newtonian/Galilean is a degenerate case of the “right” relativistic understanding.

What follows is couched in math. All the math naturally has correspondences in everyday physical behavior, but this connection can easily get lost. One way to stay to grounded is to keep the basic picture that “you” are moving around with a (real, physical) measuring stick in hand making measurements of “me,” who is likewise moving around with my own measuring stick. A clock relies on some constant velocity object moving periodically. For example, a light particle bouncing between two mirrors is a clock. To measure time, one counts the number of round trips. In this view, time is not an independent backdrop that is “just there” ticking away, it is a contraption made of physical measuring sticks and, as such, we should have no more expectation that it remains fixed than that the measuring sticks remain fixed. When we say “the geometry of spacetime,” we mean how our measuring sticks and the clocks we make out of them actually behave, and specifically, what remains invariant as our measuring sticks move about.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image116.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image117.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image118.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image119.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image120.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image121.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image122.png)

Figure 17 - A Clock is a measuring stick and periodically moving object

We know our symmetries from introspection.

1.  Translations (“is the pool table here or there, now or later”)

2.  Rotations (“is the pool table facing east or north”)

3.  Boosts (“is the pool table on a train or on the ground”)

This is the full set of actions we do to a physical system that leaves its (instinctively recognized) physics the same.

We can name the associated generators, respectively: P, H, J, K. (This group is called the Poincare symmetry group. If one removes the translational parts, it is called the Lorentz symmetry group.)

| **Symbol** | **Name** | **Invariant** | **Symmetry** | **Notes** |
|----|----|----|----|----|
| J & K & P | Full group generators | J,K,P =\> spin | Full symmetry | Spin is the invariant built from the rotation/boost tensor at a given momentum |
| P | 4-Momentum | \|P\| = mass | Translational | Mass in the invariant 4-momentum norm |
| 
``` math
P_{i}
``` | Space Momentum | n/a | Space translation |  |
| H | Energy (Time Momentum component) | H = mass | Time translation | Mass is the energy in the rest frame |
| J | Angular Momentum | \|J\| = spin | Spatial rotation | Spin is \|J\| in the rest frame. |
| K | Boost generator | n/a | Velocity boost |  |

Table 1 - Spacetime Generators

Our next step is to capture how these symmetry components interact with each other in their commutators. Below is a table of the commutators that govern the physical behavior we observe. These commutators express what we already intuitively grasp about the symmetry of physical behavior, or, in some cases, what we would grasp if we lived at the scale of maximum (light) speed

| **Commutator** | **Meaning** |
|----|----|
| \[ Pᵢ , Pⱼ \] = 0 | Stepping in one direction has no influence on perpendicular directions. |
| \[ Pᵢ , H \] = 0 | Stepping in any direction has no influence on time. |
| \[ Jᵢ , Jⱼ \] = εᵢⱼₖ Jₖ | Rotating around one axis then another causes a rotation around the third. εᵢⱼₖ just keeps track of “clockwise” vs “counterclockwise.” |
| \[ Jᵢ , H \] = 0 | Rotating around any axis has no influence on time |
| \[ Jᵢ , Pⱼ \] = εᵢⱼₖ Pₖ | Rotating around any axis and stepping in the direction tangent to rotation around another axis causes a step in the direction tangent to rotation around the third axis. |
| \[ Jᵢ , Kⱼ \] = εᵢⱼₖ Kₖ | Rotate in one direction and boost velocity in the direction tangent to rotation in another causes a boost in the direction tangent to rotation about the third axis. |
| \[ Kᵢ , H \] = Pᵢ | x = vt : boosting velocity along one direction, then taking a step in time causes a step along that direction. |
| \[ Kᵢ , Kⱼ \] = (+/−)(1 / c²) εᵢⱼₖ Jₖ | Boost in direction, then in the perpendicular direction and this causes a rotation about the axes in the third direction. Here we have a choice of whether this sign should be positive or negative. It’s hard to see here, but if you go through the following steps, you will find that choosing a positive sign leads to a hyperbolic space with a speed limit of c, while a negative sign allows for infinite speeds. Ultimately this choice comes down to which you believe. If positive, you believe in the finite, invariant speed of light and local causality. If negative, you believe velocities can add to infinity, contradicting experiment and implying action at a distance. |
| \[ Kᵢ , Pⱼ \] = (1 / c²) δᵢⱼ H | Boosting velocity in one direction has no impact on translation in a different direction (i != j), Boosting in one direction and taking a step in that direction has causes a step forward in time. All the other commutators are intuitive from everyday experience. This one is not because c is so large for humans that this appears to be zero in everyday experience. But note that if we assume c is infinite (matching our “slow/heavy” perspective), this says that a step in time has no influence on a step in position. So we at least know this relation is intuitive at our scale. But with a little imagination, we can appreciate that is intuitive at any scale if we read as saying that as we boost toward c, the H and P grow in unison toward infinity, pushing event farther and farther apart in time and space |

Table 2 - Poincare group commutators

Before we move on, it’s helpful to “solve” the commutation relations to arrive at the actual mathematical definitions of the generators in terms of vector fields, i.e., fluid flows.

| **Generator** | **Vector flow**              |
|---------------|------------------------------|
| P             | ∂/∂xᵢ                        |
| H             | ∂/∂t                         |
| J             | εᵢⱼₖ xʲ (∂/∂xₖ)              |
| K             | t (∂/∂xᵢ) + (xᵢ / c²) (∂/∂t) |

Table 3 - Generators realized as vector fields

From the commutators above, we can find the invariant metric for our physical space. First, we demand that invariance must hold for every generator. That is to say, no matter how our symmetry moves us, wiggling a bit with any generator does not change the invariant inner product. Note that metric is only on translations, not in-place symmetries of our reference frame. Therefore, we only need to move about every translational symmetry and test our generators there. That is:\
\
$`\left\langle e^{\theta X}Y,\text{ }e^{\theta X}Z \right\rangle\text{ is independent of }\theta\left( \forall\text{ }Y,Z \right)`$, where X is every translation generator and Y and Z are all combinations of generators (including translation generators).\
\
$`e^{\theta X}`$ moves us along a translation direction, while X (or Y) wiggles us in some symmetry direction. And \<.,.\> just is our inner product we want to find.\
\
This independence condition requires the derivative with respect to $`\theta`$ to be 0. Using the expansion of the exponent in terms of commutators we saw above and the chain rule, one arrives at:

⟨\[X,Y\],Z⟩+⟨Y,\[X,Z\]⟩=0 ​  ∀Y,Z

Let’s come back to this in a second. We don’t need to rigorously solve this equation for every combination of commutators to find most of the elements in our metric matrix g. In fact, we can find all elements up to fixing a single independent parameter. (Guess what that parameter is, physically?)

1.  The 3x3 block matrix in the lower right acts on spatial vectors. From ⟨Pᵢ , Pⱼ⟩ = C δᵢⱼ, we know that:

> ⎡ C 0 0 ⎤
>
> ⎢ 0 C 0 ⎥
>
> ⎣ 0 0 C ⎦
>
> this is just our familiar metric for the dot product, up to a scale factor of C.

2.  Furthermore, because time and spatial generators don’t mix, we know all the cross-terms vanish.

3.  Finally, \<H, H\> is some constant, call it A. With this we have

> g = ⎡ A 0 0 0 ⎤
>
> ⎢ 0 C 0 0 ⎥
>
> ⎢ 0 0 C 0 ⎥
>
> ⎣ 0 0 0 C ⎦

Now all we have to do to find the metric is to determine A/C, and to do this, we use the identity:\
⟨\[Kᵢ , H\], Pⱼ⟩ + ⟨H , \[Kᵢ , Pⱼ\]⟩ = 0\
\
From which we find:\
⟨\[Kᵢ , H\], Pⱼ⟩ + ⟨H , \[Kᵢ , Pⱼ\]⟩ = 0

⇒ ⟨Pᵢ , Pⱼ⟩ + (1 / c²) δᵢⱼ ⟨H , H⟩ = 0

⇒ C δᵢⱼ + (1 / c²) δᵢⱼ A = 0

⇒ A = −c² C

Thus giving the metric:\
g = ⎡ −c² 0 0 0 ⎤

⎢ 0 1 0 0 ⎥

⎢ 0 0 1 0 ⎥

⎣ 0 0 0 1 ⎦

Since this matrix is diagonal, we can easily read off the invariant interval between events:\
\
s² = −c² Δt² + Δx² + Δy² + Δz² = −c² Δt′² + Δx′² + Δy′² + Δz′² .

And there you have it! This shows that the speed of light is not “the speed of light,” but the factor relating space to time in the definition of the invariant interval that all observers can agree upon.\
\
But let’s keep playing this out. Every generator is a matrix that acts on a spacetime vector. We already know what all the generators other than boosts do from our intuitive “slow person” perspective, but we need to work out the boost matrixes.

The worldline is the path a frame’s origin follows in t, z, y, z spacetime. as viewed by any frame. A velocity boost in spacetime is a rotation of the world line.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image123.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image124.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image125.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image126.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image127.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image128.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image129.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image130.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image131.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image132.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image133.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image134.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image135.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image136.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image137.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image138.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image139.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image140.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image141.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image142.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image143.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image144.png)

Figure 18 - Worldlines, velocity, rapidity

The metric for a symmetric space is defined as follows -- If you take a step, measure two vectors’ inner product, and come back, that will be the same as if you had stayed and measured the same two vectors. The metric counterbalances the interplay of the directions as the symmetry is preserved. That is, the rulers you carry may stretch this way or that as you speed up, but there is a mathematical ruler that varies with the symmetry so that frames agree. And that invariant value is whatever the physical measuring stick the observer at rest reads.

This leads to the following derivation of the “Lorentz” transformation that transforms time and space coordinates as relative velocity increases:\
\
Let g = ⎡ −c² 0 ⎤ , Λ = ⎡ A B ⎤ and impose Λᵀ g Λ = g .

⎣ 0 1 ⎦ ⎣ C D ⎦

From Λᵀ g Λ = g:

−c²A² + C² = −c²

−c²AB + CD = 0

−c²B² + D² = 1

At this point, there are two ways we can parameterize the Lorentz transformation. In either case, our parameter is the (local, infinitesimal) slope of the world line. The first option is to use velocity. This grounds us in familiar physical concepts but obscures the geometry of spacetime. The other option is to use the rotation angle $`\eta`$. This obscures the familiar role of velocity as the dx/dt, but makes the geometry of spacetime more transparent. In any case, the two approaches are related by the identity:\
``` math
\tanh(\eta) = \frac{v}{c}
```

Let’s proceed using velocity first. Acting with Λ on (x, t) we have

t' = A t + B x

x' = C t + D x\
\
If we set x’ to be the origin of the primed frame and recognize that x/t is just velocity, we have:\
x' = 0 ⇒ C t + D x = 0 ⇒ v := dx/dt = - C/D\
\
From here it is really just algebra to arrive at:\
\
$`\Lambda = \begin{bmatrix}
\gamma & - \left( \frac{v}{c^{2}} \right)\gamma \\
 - \nu\gamma & \gamma
\end{bmatrix}`$ with $`\gamma = \frac{1}{\sqrt{1 - U\frac{2}{c^{2}}}}`$

If we now use $`\tanh(\eta) = \frac{v}{c}`$ and some hyperbolic trig identities, we find that

Λ(η) = ⎡ coshη −sinhη / c ⎤

⎣ −c·sinhη coshη ⎦

This is showing us something quite amazing. When ordinary rotation matrices rotate a coordinate system, the vector separating any two points traces a circle. In hyperbolic Minkowski spacetime rotation, when the rotation matrix rotates the coordinate system the vector separating two points traces a hyperbola. This means that the separation vector’s components grow toward infinity as the rotation pushes toward the hyperbola’s asymptote. ![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image145.png)That asymptote is the c, the speed limit at which the time and space components of event separation go to infinity.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image146.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image147.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image148.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image149.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image150.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image151.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image152.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image153.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image154.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image155.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image156.png)

Figure 19 - Separation vector traces a hyperbola

Let’s picture an object’s path in spacetime as being pushed around by a fluid flow. As the object “turns toward” greater speed, the farther ahead you are, the yet farther ahead you become as the flows pick up as you go. This flow can measure displacements by virtue of testing how would act on them. These measuring sticks corresponding to the flows are the same as the displacements, but for that one is, in matrix language, the transpose, in fluid flow language, the way separated particles get pushed around by a flow. The space of these measuring sticks is the generator, or momentum space. Generator space is the flipside, or dual, of tangent, or interval, space. With this in mind, naturally generators have the same geometry as intervals do. Thus, we have

$`\begin{array}{r}
\Delta t^{2} - \Delta x^{2} = const1\left\langle = \right\rangle \\
\Delta E^{2} - \Delta p^{2} = const2
\end{array}`$

The value of const2 is telling us how much energy, or time generation, the object has at rest, that is, where the hyperbola crosses the E axis. This is identical to mass up to a scale factor in c, requiring more change in momentum to make a given change in energy. This of course is then:

E = mc^2

There is an inevitability to the structure of spacetime. There are only so many possible linear transformations on spacetime coordinates. There are space-only shears, which is the Galilean, pure rotations, which leads to a non-physical world where in which nothing differentiates time and space, and hyperbolic rotations, which impose a limiting asymptote that matches the observed constancy of light speed and supports the notion there is no causality other than local causality, a point can only be influenced by its neighbors.

## Outline

1.  Set up the paradox

    1.  All observers agree on length and time, example of rigid bodies, clocks

    2.  Principle of rel – no rest

    3.  Show that this leads to frame dependent light speed

        1.  Right out transformation rules

        2.  Show it

    4.  Speed of light frame independent

2.  Resolve the paradox

    1.  Resolution is in transformation rules

    2.  Light and space bend such that c is frame independent

    3.  Length contraction time dilation (why dilation) – non-math

    4.  Goal will be to show that with new transformation light speed is constant

3.  Geometry

    1.  Move from Galilean transform to Lorentz

        1.  Show spacetime

        2.  Define worldlines (nothing relativistic yet)

        3.  Note spacetime is just a way of graphing, applies to G and E. What makes spacetime one thing in Relativity is that the coordinates mix symmetrically

    2.  Minkowski space

        1.  Show Gal. trans in spacetime (gif) (what is this? Ask gpt? Worldline rotates along the shear?)

        2.  Show Lorentz trans. (gif) (just teaser, explaining the transform will folow)

        3.  Point out that to see the effect of the transformation you need to the orientation of world line and two events on it to see how their separation changes.

        4.  New symmetry – relative velocity

        5.  Symmetry is hyperbolas

        6.  Invariant is t-squared – x-squared, which is just equation for hyperbola

            1.  Define proper time

            2.  Give interpretation of it

            3.  Point out it becomes new parameter – so all our coordinates (space and time, momentum and energy) are still parameterized.

        7.  Define t axis as ct, will see why this is justified one we works thing out, for now we can just say, axes have to be same units to define length

        8.  Revisit the Lorentz transform (with good diagrams/gifs)

            1.  A point on world line traces out hyperbola under boost

            2.  C is 45 degrees

            3.  All objects move at c in spacetime

            4.  Rotating past C would give negative separation

                1.  This sets the speed limit

            5.  Minkowsk space regions, only “timelike” accessible

            6.  X and t axes fold together

                1.  This justifies putting c on the time coordinate, at light speed time and space are same thing.

                2.  “where does a light speed object move in such and such time “ is a non-physical question. This paradox resolved as light is delocalized

                3.  has no rest frame

                    1.  which causes transverse polarization.

            7.  Events in rest frame separate infinitely when boosted to light speed.

                1.  Warrants “light has no time passage, can’t connect events”

        9.  Show transforming a point in spacetime using hyberbolic rotation matrices

            1.  Define rapididty and give an interpretation of

            2.  Compare to normal rotation matrices

            3.  Aside, hyperbolic trig and normal trig are both exponentials, with and without a complex number

            4.  Derive Lorentz transformation

    3.  Light cones - Causality

        1.  Draw example on world lines

        2.  Show this is objects past and future

        3.  Light cones stay fixed under boosts

        4.  \[ask gpt\] how to interpret what not having worldline in center of light cone means, it seems to affect your history, but is observer dependent.

            1.  And what being on the light code (light) means.

        5.  Light cones from an absolute causal structure onto spacetime irrespective of relative motion

4.  Twin paradox

    1.  Provides evidence that malleability of time is real

    2.  Not a paradox, makes sense in the theory and has been measured over and over

    3.  Related to non-inertial motion – inertial – dilation is just perspective

    4.  Show how it works with diagramming – turning around leads to travelling twin skipping over events in inertial twins world line.

    5.  Express this in terms of light cones (how, needs research)

5.  Dynamics

    1.  Find equations for momentum by just plugging 4-velocity

        1.  Derive 4-velocity

        2.  Derive momentum

        3.  Show association on time-component momentum to energy using first order expansion of time component under boosts

        4.  Show this leads to famous e=mc-squared in rest frame

    2.  Show what momentum space looks like

        1.  Objects of a given mass live on hyperbolic mass shells

    3.  Show that Newton is not relativistic

        1.  Fμ=dτdpμ​

    4.  Derive momentum space from symmetry principles

        1.  Doesn’t require putting mass in by hand

        2.  Aligns with quantum theoretic way of thinking of physics

        3.  Work it out

            1.  Find generator of translations using first order expansion technique

            2.  Show eigenfunctions of this generator are plane waves

            3.  Plane wave have a free parameter

            4.  This leads to a dual space to Minkowski space of plane waves

            5.  Choosing the parameter fixes the shell

            6.  Boosting transforms along the shell

            7.  Mass is the invariant distance, the 4-momentum casimir operator

6.  Action

    1.  Show action for a free particle maximizes proper time

    2.  Interpret this in light of twin paradox and light cones as maximizing “causal area”

7.  Spacetime symmetries

    1.  Poincare group

        1.  Translations

        2.  Boosts

        3.  Little group

    2.  Mass is invariant associated with translations

    3.  Spin is invariant associated with little group

        1.  Shows up in everyday life as polarization

        2.  Polarization only 2d because light has no rest frame – can’t rotate in direction of travel

## The Path of Reasoning to Relativity

If Quantum Mechanics is supremely weird and hard to accept, Relativity is supremely elegant and makes the weird feel normal, drawing conclusions that tear down instinctual expectations and help build new ones from careful reasoning alone. We’ve seen how this is done in the math of generators, but the purpose of that discussion was more to demonstrate that Relativity can be derived from an understanding of nature’s symmetry and less to build intuition and follow the kind of natural reasoning that guided Einstein . Let’s now take a more standard approach to understanding Relativity.

Let’s dive into the physical reasoning. There are three things we expect to be true about the physical world.

1.  There is no preferred “rest frame.” This is the “Principle of Relativity” that dates not to Einstein, but to Galileo. A person on the ground watching a train go right is no more at rest than a person on the train watching the ground go left. This becomes obvious when one notes that the earth itself, and the solar system, the galaxy, etc. are all moving. What would we ever call “at rest”? This relativity of “inertial reference frames” requires physical laws to be true in all frames since no one frame is preferred. This adds a new symmetry to the more obvious ones of time, space, and rotation, the symmetry of relative constant velocity. This accords with our instinct that, say, a pool game on a train behaves just as a pool game on the ground.

2.  Time and distance are fixed for all observers. Let’s be specific about what we mean by this. If we build two rulers that are identical and give one to a person on the ground and another to a person on a train, then ask the two people to measure each other’s rulers as they pass one another, we expect they will both measure each other’s rulers to be 12” long. Likewise if we give both people synchronized clocks and ask them to record the time the ruler takes to pass by, we expect they will report the same time.

3.  Velocities add. That is, if a pitcher throws a ball at 100 mph, and you put them on a train at 100mph, and you put that train on another train at 100mph, the ball will go 300mpm as viewed from the ground. And there is no limit to this.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image157.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image158.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image159.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image160.png)

> ![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image161.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image162.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image163.png)
>
> ![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image164.png)

Figure 20 - Velocities stack

In order to abide both these conditions a **Galilean Transformation** between our train and the ground is as follows:

``` math
\begin{array}{r}
t' = t \\
x' = x - vt
\end{array}
```

One can see that time is the same in both frames. While x changes with time, the distance between two locations does not:

``` math
\left( x_{2}' - x_{1}' \right) = x_{2} - vt - \left( x_{1} - vt \right) = x_{2} - x_{1}
```

These transformations also preserve Newton’s 2<sup>nd</sup> law, the definition of “physics staying the same” as follows

``` math
F = m\frac{\mathbb{d}^{2}x}{\mathbb{d}t^{2}} = m\frac{\mathbb{d}^{2}(x - vt)}{\mathbb{d}t^{2}} = \frac{{m\mathbb{d}}^{2}x}{\mathbb{d}t^{2}}
```

So these transformations fulfill the three truisms above. But there is a problem! Velocities do not stack up. There is a limit, c, 300,000 m/s, the speed of light. Let’s be clear, this doesn’t mean our pitcher can’t ever throw faster than 300,000 m/s. It means something much stronger and more counterintuitive. It means that if our pitcher throws 200,000 m/s, and you put him on a train going 200,000 m/s, the ball speed you measure on the ground will not be 400,000 m/s, but will be something less than 300,000 m/s.

We simply cannot maintain our first two truism, the equivalence of all frames and the immutability of measuring sticks and, at the same time, have a frame independent maximum speed. Something has to give. The choice Relativity makes is to keep the Principle of Relativity and do away with the notion of fixed time and space separation. That this is the right choice may be argued by saying that it is self-evident that nature behaves the same way in all inertial frames, but the greater evidence that it is the right choice is the perfect success of Relativity in describing the world at all speeds.

If we allow space and time separation to vary between inertial frames, but require that speed of light remain constant, we are led naturally to equations that show how space and time separation transforms between inertial frames. The “**Lorentz Transformations”** that specify how space and time coordinates transform can be derived surprisingly easily by imposing that light speed is constant in all frames, our symmetry-first approach being one such derivation, but the essence of the transformation is this – while velocities do appear to plainly stack at everyday speeds, eventually that stacking approaches an asymptotic value of c, and rather than space and time separation being fixed for all frames, they grow with relative velocity in exact proportion to each other. We will derive this transformation from a geometric view that makes the structure of spacetime transparent. What we will see is that a hyperbolic transformation of time and space separations yields both the properties we want – an asymptotic approach to c and the proportional scaling of spatial and temporal distances.

As we work through the geometric picture, we will show several of the famous results of Special Relativity.

1.  c is the maximum speed of any object

2.  The time between two events in an object’s rest frame is less than the time measured in any moving frame.

3.  A “twin” that makes a light speed round trip will age less than the twin who “stayed home.”

## The Geometry of Relativity

The stage for relativity is spacetime, which has two senses. In one sense, it is nothing new, it is just a way of representing motion. Rather than attaching a clock at every point in a chart of space alone, we give time its own axis and show the path of an object through space and time in one “space.” (“Space” is an overloaded term. It means physical 3d space, but it also means any mathematical vector space.) The path through this space is an object’s **world line**. Note that an object always moves in spacetime, for, even if it is not moving in position space, it is moving along the time axis. Obviously spacetime is 4 dimensional, but we will often deal with a single spatial dimension to allow for a 2d drawing.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image165.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image166.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image167.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image168.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image169.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image170.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image171.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image172.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image173.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image174.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image175.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image176.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image177.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image178.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image179.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image180.png)

Figure 21 - Time as a parameter or as coordinate are equivalent

Before discussing relativistic spacetime, let’s look at what Galilean transformations look like in our “classical” spacetime.

<figure>
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image183.png" />
<figcaption aria-hidden="true"><p><img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image145.png" /><img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image181.png" /><img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image182.png" /></p></figcaption>
</figure>

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image184.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image185.png)

<figure>
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image192.png" />
<figcaption aria-hidden="true"><p><img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image186.png" /><img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image187.png" /><img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image188.png" /><img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image189.png" /><img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image190.png" /><img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image191.png" /><img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image192.png" /><img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image193.png" /><img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image194.png" /><img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image195.png" /><img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image196.png" /></p></figcaption>
</figure>

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image197.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image198.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image199.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image200.png)

Figure 22 - Galilean Transformation are Spacetime shears with v = dx/dt

This transformation is a “shear,” in the language of linear algebra. As indicated on the diagram, we see that it preserves both temporal separation, while spatial separation increases by $`vt`$.

We need to replace this transformation with something that sets c as an upper bound. We know we must have a linear transformation as the constant velocity worldline must stay straight under transformation and the origin is unchanged. Possible transformations other than shears are rotations or hyperbolic rotations. Before proceeding, let’s multiply the units on the time axis by c. We are free to do this as it is just a constant scaling, and it is necessary to show how worldlines of different angles equate to different velocities. (Alternatively, you can put see in the metric tensor g as we did during the symmetry discussion.) The justification for treating time as another distance will become clear.

We can reject spherical rotations. First, velocities can go to infinity. Second, space and time vary in inverse proportion to each other, which will lead to decidedly unphysical behavior.

This leaves us with hyperbolic rotations. Let’s look again at hyperbolic rotations. It’s easiest to see visually.

<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image201.png" style="width:4.52801in;height:3.27795in" alt="A screenshot of a video AI-generated content may be incorrect." />

In this diagram, the tick marks along the hyperbola are the hyperbolic angle. Just as an angle in normal rotations is proportional to an arc length, the hyperbolic angle is proportional to a segment length on the hyperbola. This angle, $`\eta`$ we saw before is called **rapidity** in Relativity, and, as it goes to infinity, and as an object accelerates without bound, the orientation of the world line approaches the asymptote at 45 degrees. The value of the velocity along the 45-degree asymptote is simply x = ct, or v = c, setting our speed limit in geometric framing.

Using this rational, we justify the hyperbolic rotation matrix we found earlier.

``` math
\begin{bmatrix}
\cosh\eta & - \sinh n \\
\sinh\eta & \cosh\eta
\end{bmatrix}
```

Where $`\eta`$ , the hyperbolic angle, again, is defined by $`\tan(\eta) = \frac{x}{ct}`$ and $`\frac{x}{ct}`$ is the slope of the worldline. The rotation matrix moves any interval on a worldline along a hyperbola. When we carry out the action of the rotation matrix on a spacetime vector:\
\
``` math
\left\lbrack \begin{array}{r}
ct' \\
x'
\end{array} \right\rbrack = \begin{bmatrix}
\cosh\eta & - \sinh\eta \\
 - \sin\eta & \cosh\eta
\end{bmatrix}\left\lbrack \begin{array}{r}
ct \\
x
\end{array} \right\rbrack
```

This transformation replaces the position-only shear of Galilean transformation with a time and space mutual “scissoring”:

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image202.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image203.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image204.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image205.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image206.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image207.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image208.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image12.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image192.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image209.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image210.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image192.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image211.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image212.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image213.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image12.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image192.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image12.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image12.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image214.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image215.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image216.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image217.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image12.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image12.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image192.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image218.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image219.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image220.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image221.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image222.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image223.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image224.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image192.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image225.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image226.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image12.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image12.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image227.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image228.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image12.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image229.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image230.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image231.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image232.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image233.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image65.png)

Figure 23 - time and space shear together in spacetime

*Rotations and Hyperbolic rotations are exponentials*

*How are hyperbolic and regular trig functions related. As we’ve seen, they are both rotations of a sort, one that traces a circle, the other that traces a hyperbola. But let’s ask, what function goes to infinity quickly as its argument goes to infinity? And what function traces a circle as its argument goes to infinity? These are exponentials:*

$`\mathbb{e}^{x}`$ *and* $`\mathbb{e}^{\mathbb{i}x}`$

*And, in fact trig and hyperbolic trig functions are defined in terms of these exponentials, for example:*

$`\sinh(x) = \frac{\mathbb{e}^{x} - \mathbb{e} - x}{2}`$

``` math
\sin(x) = \frac{\mathbb{e}^{\mathbb{i}x} - \mathbb{e}^{- \mathbb{i}x}}{2}
```

Before, in the symmetry section, we derived the Lorentz transformation directly from symmetry and showed this we equivalent to the hyperbolic rotation matrix. We can go the opposite direction, and having argued for the hyperbolic rotations, we can use trig identities to find the Lorentz transformations, which famously demonstrate “time dilation” and “length contraction.” (In fact all measuring sticks expand when boosted as both $`\Delta t`$\
and $`\Delta x`$ grow when boosted. Length “contraction” is an artifact of the how time change impact length measurements.

$`x' = \gamma\left( t - \frac{v^{}}{c^{2}}x \right);\gamma = \frac{1}{\sqrt{1 - v\frac{2}{c^{2}}}}`$

``` math
t' = \gamma\left( t - \frac{v}{c^{2}}x \right)
```

This is really quite remarkable. We were able to derive the Relativistic expression for time dilation and length contraction simply from reasoning about which transformations could fulfill our requirements.

We now have a much more physical definition of spacetime. It is not just a way to plot the path of an object. It is actually a unified space in which time and space mix as coequals. We will add even more physical heft to this when we see that our equations of motions, such as Newton’s second law, are not valid in 3-space, but are in spacetime.

We can see that the hyperbolic rotation matrix acts on the x and ct axes such that, ss $`\eta`$ approaches infinity, the time and space axes “scissor in” toward each other until, at c, they meet. What is this telling us. It is saying that for an object a light speed there is no difference between time and space. We will be able to add more depth to this idea in a bit, but for now it shows us the justification for scaling the time axis by c to be ct. For a light particle, there is not difference between time and space, so they must have the same units, be the same expression of distance.

### Invariance

Our physics, our equations of motion, are invariant under Lorentz, or hyperbolic, transformations. This is a symmetry. As we discussed earlier, any symmetry is marked by some invariant. Our equations of motions are that invariant, but there is a simpler invariant built into the geometry itself, and that geometric invariant maps to “physical invariance,” as we will see. For both translational and rotational symmetries the geometric invariant is angle and length (or “interval” more generally), packaged into the dot product. As our representation of rotations is in 2 dimensions, the invariance includes components from x and y as is given by the Pythagorean theorem. For translations, it is just the separation of two points. For hyperbolic rotations, the geometric invariant is the hyperbolic equivalent of the Pythagorean theorem. The table below summarizes

| **Symmetry**        | **Invariant**                      |
|---------------------|------------------------------------|
| Translation         |                                    
                       ``` math                            
                       \Delta x;\Delta t                   
                       ```                                 |
| Rotation            |                                    
                       ``` math                            
                       \sqrt{\Delta x^{2} + \Delta y^{2}}  
                       ```                                 |
| Hyperbolic Rotation |                                    
                       ``` math                            
                       \sqrt{\Delta t^{2} - \Delta x^{2}}  
                       ```                                 |

Table 4 - Invariants in translational, rotational, and hyperbolic symmetries

Just as the equation for a circle is given by $`r^{2} = x^{2} + y^{2}`$, the equation for a (vertical) hyperbola is given by $`y^{2} - x^{2} = a^{2},\ a`$ being where the hyperbola intercepts the y-axis. To measure distances, or separation between points, we must consider the coordinates of two points.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image234.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image235.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image236.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image237.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image238.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image239.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image240.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image241.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image242.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image243.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image244.png)

Figure 24 - Graphing the hyperbola equation

Applying this geometry to relativity, we have, as we’ve already seen the invariant:

``` math
s^{2} = \left( c\Delta\left. 〖t \right) \right.〗^{2} - \Delta x^{2}
```

Or, in its more general form:\
``` math
\Delta x^{u}\Delta x_{\mu} = s^{2}
```

This is the “Minkowski invariant interval.” The all-important implication of the minus sign in the invariant interval is that as the hyperbolic rotation matrices act to boost relative velocity, the separation between events, while equal in spacetime due to this odd metric, grow hyperbolically in measured spatial and temporal separation. It may seem crazy that we define a length-like interval that clearly changes as we draw it on paper invariant, but this is valid in geometry and yields transformations that preserve physical behavior. This expanding separation in spatial and temporal space leads to the conclusion that for objects at light speed, events are infinitely separated in time, which we interpret by saying there are no events. They can experience no passage of time, nor experience an ordering of events, emission and absorption of a photon is the same event from a photon’s perspective.

### Proper Time

We can now define and interpret a new quantity, “**proper time**”:

``` math
\tau = \frac{1}{c\int\mathbb{d}S}
```

To make sense of this term, consider an object’s rest frame. Here ds is just c(dt), so $`\tau`$ is just t. And this is exactly what proper time is – the time in an object’s rest frame. It is the time we always measure between events in our rest frame. Thus the invariant path length just *is* the proper time. Although we only measure proper time between events in our rest frame, we can agree on each subject’s proper time. This allows proper time to replace time’s role as a **parameter** in term of which all other variables are written.

$`t(\tau) = \tau\cosh(\eta);x(\tau) = c\tau\sinh(\eta)`$

We can also find the velocity in spacetime, now that we have a distance and time:

``` math
u = \frac{\mathbb{d}s}{\mathbb{d}\tau} = c\ 
```

Everything in spacetime moves at the same speed c.

### Physical Invariance

We know that a body in an inertial frame is “free.” It is not “compelled” by any “forces.” At least for the case of a free particle, if we can say that it maintains constant velocity, we have accurately captured its physics. But what is the condition for traveling at constant velocity? It is that the body’s path is a straight line, and the condition for a straight line, it can be shown straightforwardly, is that the proper time is maximized. (Just a the “shortest” path is a line in Euclidean geometry, the “longest” path is a line in Minkowski geometry, due to its hyperbolic structure. We then capture the invariant physics completely via the maximization of proper time. Thus we see, miraculously, that the symmetry of physical behavior is contained entirely in the geometry of spacetime. Later, we will extend this idea to the case when there are forces involved.

### Light Cones

From a given point in space time, you could sit still and move forward along the t axis. You could speed up to the right up to the speed of light and go along the t = x asymptote. Likewise, you could speed up to the left up to the speed of light and proceed along the t = -x asymptote. These are the only places you can go. Likewise, the only places you could have “come from” are similarly bound by the light speed asymptotes. This region of spacetime that you can access is called the **light cone**.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image245.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image246.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image247.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image248.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image249.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image250.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image251.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image252.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image253.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image254.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image255.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image256.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image257.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image258.png)

Figure 25 - Light cones

This structure shows that there is no notion of two locations sharing the same time. At the vertex of our light cone, any step to the left or right is unreachable. “something happened here and there now” is statement that has no meaning. Light cones impose a causal structure on spacetime. We are familiar with idea that we cannot say what is happening at a distant star in the near past because of the time light takes to travel. But it is not just that light cannot travel faster than c, but that no causal connection can exist that requires greater-than-lightspeed. In this sense, the biggest message Relativity delivers is not the fact that light travels at c in all frames, or even that time and space coordinates are not a fixed background, but that there is a causal structure in the universe represented by light cones in spacetime. The implication is very strong. It says that there is no possibility of influencing an event without being at that event’s location. Before any coordinates or transformations, this is the structure spacetime – at every event there is a cone of causal influence. The path you traverse is choosing which cones you visit.

### Twin Paradox

Relativity predicts that if you and your twin live together on, say, earth, and your twin leaves on a high-speed vessel for a long trip and returns to meet you, you will have aged more than they have. This is counterintuitive, as Relativity generally is. But it is doubly so because it seems to indicate that the earth is a preferred rest frame, which violates the Principle of Relativity. Sure, the twin in motion appears to elapse less time to the twin on earth, but shouldn’t the same be true for the travelling twin – that the twin on earth appears to elapse less time than him? The resolution lies in the fact that to turn around, the travelling twin has follow a non-inertial (not constant velocity) trajectory. The result is very much real and is in fact used in everyday life to correct for the non-inertial motion of GPS satellites. Understanding how this works geometrically is instructive in itself, but also has fascinating implications.

The following discussion uses snapshots and a nearly exact reproduction of the argument in the video: [Complete Solution To The Twins Paradox](https://www.youtube.com/watch?v=0iJZ_QGMLD0)

Imagine that Romulus stays on earth and travels forward 10 seconds on his worldline along the time axis. He sees Remus leave, turns around at 5 seconds, and returns at 10 seconds.

<figure>
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image259.png" style="width:6.5in;height:3.93958in" alt="A graph on a white paper AI-generated content may be incorrect." />
<figcaption><p>Figure 26 - Twin travels, turns around, comes back</p></figcaption>
</figure>

Now, let’s say that the Remus is travelling at 0.6c. In that case

$`\tau = t\sqrt{1 - \frac{v2}{c^{2}}} = 8`$

<figure>
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image260.png" style="width:4.36134in;height:3.54185in" alt="A screen shot of a graph AI-generated content may be incorrect." />
<figcaption><p>Figure 27 - 8 seconds pass according to the travelling twin's clock</p></figcaption>
</figure>

However, since there is no preferred rest frame, Remus thinks Romulus’ proper time is given by the same equation. Just as Romulus multiplies his proper time by 0.8 to get Remus’ proper time, so does Remus multiple his proper time by 0.8 to get Romulus’ proper time. Since Remus’ proper time is 8 seconds, he believes that Romulus’ is 6.4 seconds. However we have to divide this into two sections, each of 3.2 seconds because, when Reemus turns around, his time axis transforms in the opposite direction. This is seen in the picture below.

<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image261.png" style="width:5.04193in;height:3.70852in" alt="A screenshot of a video AI-generated content may be incorrect." />

Figure 28 - Travelling twin "misses" some of earth twins time

But, as we see in the picture, Remus simply never sees Romulus’ history from 3.2 seconds to 6.8 seconds. Thus, when Remus returns, he has aged 8 seconds while Romulus has aged 10 seconds. Those 3.6 seconds are outside Remus’ light cone. The implication here is that non-inertial motion “misses out” on events that inertial bodies “see.” There’s something poetic about this, freedom allows the most experience, compulsion narrows horizons.

## Relativistic Mechanics

In our discussion about Relativity from symmetry, we discussed momentum space. Let’s revisit this, now taking a more elementary perspective in which we start from the definition that momentum is mass times velocity. The procedure here is straightforward. Where before we had 3 position coordinates that we parameterized by time, we now have 4 spacetime components that we parameterized by proper time.

Let’s define a subscript $`\mu`$. This is just an index that runs from 0 to 3, where 0 is the time component and 1,2, 3 are the three space components. With that in mind, we have 4-position:

``` math
x_{\mu} = (t,\ x,\ y,\ z)
```

Next, we have 4-velocity:

``` math
U_{\mu} = \frac{\mathbb{d}x_{\mu}}{\mathbb{d}\tau} = \frac{\mathbb{d}(ct)}{\mathbb{d}\tau},\frac{\mathbb{d}x}{\mathbb{d}\tau},\frac{\mathbb{d}y}{\mathbb{d}\tau},\frac{\mathbb{d}z}{\mathbb{d}\tau}
```

And finally, momentum:

``` math
P_{\mu} = mU_{\mu} = m\left( \frac{\mathbb{d}(ct)}{\mathbb{d}\tau},\frac{\mathbb{d}x}{d\tau},\frac{\mathbb{d}y}{\mathbb{d}\tau},\frac{\mathbb{d}z}{\mathbb{d}\tau} \right)
```

Replacing proper time with measured time, and making the association that the time momentum component is energy, we have:\
``` math
{\overline{p} = \gamma mv
}{E = \gamma mc^{2}}
```

``` math
\gamma = \frac{1}{\sqrt{1 - \frac{v^{2}}{c^{2}}}}
```

We can see that as velocity approaches c, p and E approach infinity. But going in the opposite direction, where v \<\< c, with a little power series expansion, we can find:

``` math
\overline{p} = m\overline{v}
```

``` math
KE = E - mc^{2} = \frac{1}{2}mv^{2}
```

### Relativistic Force and Dynamics

We haven’t discussed the notion of “force” or “dynamics” yet. But you probably know from high school physics or common sense that objects don’t always travel at the same velocity, that they are acted upon and change speed and direction. That is, you have probably seen:

``` math
F = ma = m\frac{\mathbb{d}^{2}x}{\mathbb{d}t^{2}}
```

This equation does not work with Relativity at face value because it treats time (t) as a frame independent parameter, which we know it is not. As we accelerate, t must itself be transformed.

The prescription for arriving at new equations of motion should not be surprising at this point. We specify each component of 4-momentum over all 4 components of spacetime. For example, Newton’s second law becomes:

``` math
F_{\mu} = m\frac{\mathbb{d}U_{\mu}}{\mathbb{d}\tau}
```

To switch back to the equation of motion in 3-space parameterized by coordinate time, use the relation seen above that:

``` math
t = \tau\cosh(\eta)
```

After just a bit of plugging things in, we arrive at:

``` math
\overline{F} = m\frac{\mathbb{d}}{\mathbb{d}t}\left( \frac{\overline{v}}{\sqrt{1 - \frac{v^{2}}{c^{2}}}} \right)
```

Staring at this a bit, we see that as $`v`$approaches $`c`$, the factor in the denominator blows up, so it takes ever more force to produce the same change in velocity. This is yet another expression of the central message of relativity that light speed is an asymptote for any object – as you approach $`c`$, the Force it takes to accelerate further approaches infinity.

### Spacetime Fields

To this point, we have implicitly thought of spacetime as the arena in which “rigid bodies” move about. This is useful way to build intuition about the properties of spacetime and is the way physics was generally thought of until the 1900s. But going forward, we will replace the idea of rigid bodies with the idea of **fields.** Fields occupy the entirety of spacetime. Specifically, they take a value at every spacetime point One can think of a field, by way of analogy, as fluid filling spacetime that can have waves on it. This is useful to understand what the term refers to, but the analogy breaks down. Waves in a fluid, say rippling on a pond, involve moving in some medium, moving some matter around, but spacetimes fields have no medium. They are that which is fundamental in nature and cannot therefore be made of anything else.

### Dispersion Relation

The equation giving the momentum-space hyperbola is\
(𝑬⁄𝒄)² − 𝒑² = 𝒎²𝒄²

Or, in its general form:

``` math
P^{u}P_{u} = m^{2}c^{2}
```

This is a fundamental result: it identifies the invariant mass and fixes how energy and momentum are related in any reference frame. Plane waves under Lorentz transformations obey an identical-looking relation:\
\
(𝝎⁄𝒄)² − 𝒌² = 𝝁²

𝝎 the frequency, and 𝒌 the wave number, and 𝝁 is the invariant 4-space wave number.

This should all sound somewhat familiar. In our discussion of symmetry, we said that plane waves were the eigenfunctions of translations. However, in that discussion, we didn’t impose any particular structure on our space. Recall, the eigenfunctions were:

``` math
{f(x) = \ \mathbb{e}}^{\mathbb{i}kx}
```

Now, we don’t have an arbitrary set of directions x, we have a space with a symmetry-abiding structure, and, abiding that structure, we refine our eigenfunctions to:

``` math
f(x) = \mathbb{e}^{- \mathbb{i}k_{\mu}x_{\mu}} = \mathbb{e}^{- \mathbb{i}\left( \omega t - \overline{k}\overline{x} \right)}
```

This allows us to *classify* such plane waves according to their dispersion relation, just as we can classify rigid bodies by their mass. Just as a free body must reside on a 4-momentum hyperbola selected by its mass, so a wave 4-number must reside on a hyperbola set by its dispersion constant.

Knowing the dispersion relation lets us see how relativity acts on plane waves, and the way their periodicity in spacetime naturally affords “counting off” the symmetry in terms of the phase. In physics, we need a “thing” to reflect a symmetry, and a point won't do as it is insufficient to show separation. A cluster of points, a "system," suffices, but it takes a lot of work to map it to spacetime symmetry. A wave, on the other hand, makes a great “thing.” If you know just two parameters, frequency and wave number, you know everything about how the symmetry affects the wave. It is a single thing, but it has just enough structure to reflect the symmetry. This idea of a wave object is ready for use with relativity, but relativity doesn't tell us how we should use it. What we will see when we discuss quantum mechanics is that if you define "things" as "wave functions that spacetime can act on," you not only get the structure to reflect spacetime, you get a means to classify things – fundamental particles -- on spacetime.

If we are saying that waves are a good candidates to be the simplest “thing” that transforms correctly in spacetime, and we have $`E^{2} - p^{2} = m^{2}`$ and $`\omega^{2} - k^{2} = \mu^{2}`$, and we think “things” have energy, it’s really tempting to associate $`m`$ and $`\mu`$, via some constant factor. Dimensionally, $`\mu`$ has units 1/length, and we need units of momentum. “Action” has the write units. Action is, alternative momentum \* position or energy \* time. You may have enc. You may have encountered that $`\hslash`$ is a fundamental unit that sets the scale of quantum effects. It has units of action. Were we to make the association that $`m^{} = \hslash\mu^{}`$ (setting c = 1), we would read off, separating time and position, that:

$`p = \hslash k`$ and $`E = \hslash\omega`$\
\
These are also famous results from quantum mechanics you may have seen. In them, we have the idea that frequency of a wave on spacetime sets the energy of a particle, not the velocity of rigid body.

#### Complex-Valued waves

Before we move on, we should mention that we have been writing wave equations as $`\mathbb{e}^{\mathbb{i}kx}`$ and using all the machinery of complex numbers but have been drawing them as sin/cos(x). That hasn’t really mattered up to now as you can arrive at the latter by taking the real part of the former, but in the following sections we are going to make specific use of the complex value in and of itself of plane waves. The following diagram illustrates a complex wave. Here I’m labeling the independent variable t rather than x, as I need x (and y) to represent the complex plane. A critically important thing to notice in this diagram is that (norm of the) amplitude is constant for complex waves. If we can argue (which we will) that amplitude and wave number are the only aspects of the wave with physical significance, then the phase (where in the complex plane the wave is at a given t), will become a new symmetry of the system. Engineers commonly represent plane waves like sound waves as exponentials, as they are easier to work with. They then take the real part at the end of calculations. But we are now saying we are dealing with waves that are “actually” complex valued. If that makes you a bit uncomfortable – what is a complex valued wave in the real world – welcome to the club. It will “make sense” when we get to quantum mechanics, at least in the sense that we will see why it is necessary. But what exactly a complex wave *is* will, I think, remain rather perplexing. Complex valued waves are where we bottom out in our description of fundamental physical reality, and, at some level, you simply cannot get down the fundamental building block of material without feeling it is all smoke and mirrors.

#### ![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image262.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image263.png)

#### 

#### 

#### 

#### 

#### 

Figure 29 - Complex waves

#### Spin and Internal Symmetries in Relativity

We have said that complex plane waves represent Poincare symmetry, but we have been vague about what sort of object is “vibrating.” In a way, we have been assuming that it is just the value of the wave itself. But a better way to think of the case where the thing that is vibrating is just a (complex) number is that the wave value is multiplying 1. The wave value can multiply other objects, most obviously vectors. What would an example of this be? Imagine a periodic fluctuation in wind speed. Say the wind is blowing westward and varies from 0 to 10 mph following a wave pattern. That’s it, that’s a vector valued wave, or, if you like, a wave on a vector valued field. The wave value multiplies some basis wind speed vector. The waves we are interested in are complex valued, so they multiply complex valued basis vectors. But we can in some situations turn this into a real valued vector by, as we discussed earlier, taking the real part at the end. There are other objects as well, such as “spinors,” that transform covariantly, that is, the invariant norms you define remain invariant under transformation. Our Hilbert state space is a space of the entire field, which includes the objects, be them scalars, vectors, or spinors, that inhabit the field.

We are going to methodically characterize what objects a spacetime field may evaluate to, but first it is helpful to anticipate where we are heading. For a moment, let’s go back to a rigid body picture. We have carefully examined what happens to a measuring stick under velocity boosts. But how would a spinning ball transform? We might think that rotational symmetry is separable from translations so that a rotating object is not impacted by velocity boosts. And this is in fact close to correct. However, there is a problem. While a body may rotate as a whole, each part of it is translating at different velocities, and thus transforming differently, thwarting the notion of a pure rotation. But if we shrink the body to a single point, the rotation symmetry remains, unaffected by velocity boosts. While this “shrinking to a point” is nonsensical for rigid bodies, it is natural for fields, where we have the notion of symmetries acting on every point. And it exactly this, the object that rotation symmetry acts on at a point, that our wavefunction on spacetime evaluates to. In a sense, as a wave on string traveling in the x direction evaluates to an amplitude in the y direction at each point, a wave in spacetime evaluates the rotation of that point.

The procedure we will follow is to fix the momentum of a point and ask what symmetries remain. This procedure produces a new “internal” symmetry group, in which motion itself is factored out. While it is more involved than this, a good instinct is to think that what remains is, as we just hinted, rotation. But there is a confusing subtlety here. Unlike the solutions to the momentum generator eigenvalue equation in which different solution’s eigenvalues correspond to different rates of change, because motion, in the sense of “change over time” is already factored out, the solutions to internal symmetry eigenvalue equations do not correspond to “rates of change” but to the different ways that the state of the object changes under rotation. For example, we can ask “how much rotation will return the object to it’s original state?”

This property of “how that state changes under rotation” will, in addition to mass, identify a wavefunction. Our task is to find what types of objects are admissible on the field, that is, as we just said, objects for which we can define an invariant norm under Poincare symmetry group actions. We will see, unsurprisingly, that one class of representations corresponds to massive particles, while another corresponds to massless. This aligns with our understanding of spacetime’s structure in which lightlike objects are fundamentally of a different category, in that they have no rest frame, than massive objects.\
\
Our first step is to simplify the problem by realizing that we don’t need to consider translations at all. Those move a point, while our object-value is at a point. We call the subset of Poincare actions without translation Lorentz actions, and as we saw they are represented by 4x4 matrices acting on 4 vectors.

Now we can add our restriction that we fix momentum. In the rest frame, the only momentum component for a massive object is the time component:\
\
``` math
k = (m,0,0,0)
```

Knowing that our Lorentz transform must preserve this we have:

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image264.png)

Thus, the internal symmetry group, as we argued already, is just the rotation group – called SO(3).\
\
For massless objects, things are a bit different. There is no rest frame and time and space have merged together, as we we’ve seen. Thus, whatever direction the light particle is moving the has the same momentum as the time component.\
\
``` math
{k = (k,0,0,k)
}
```
with z being the direction of travel. Skipping the details of the matrix algebra, this additional restriction leads to a 2 dimensional rotation orthogonal to the direction of travel, times a 1 dimensional translation matrix – called ISO(2).\
\
Now that we know the symmetry groups for the massive and massless case, we can find the representation (vector space) that carry them. We already know that we can represent rotations with 3 dimensional vectors. Regular “arrow-tipped” vectors form a “spin 1” irreducible representation of SO(3). It is a representation because it faithfully realizes SO(3) symmetry. It is irreducible because there is no lower dimensional subspace that stays closed under all SO(3) actions, and it has a spin value of 1 because it requires (at least) 1 full rotation to return to the same orientation. In addition to having a spin value of 1, this arrow-tipped representation can have 3 eigenvalues of a given generator, e.g., rotations about the “z” axis -- m = 1, m = 0, or m = -1, corresponding how rotations acts on the overall phase. m = 1 picks up a 2pi phase after a rotation, m= -1 picks up a -2pi phase, and m= 0, which corresponds to the axis of rotation itself. Thus, the full state of the “little group” (the group factoring out translations and fixing momentum) is given as \|l, m\>, or, for the for the case of an arrow tipped vector rotating clockwise about the z axis, \|1, 1\>. \[We need to introduce Dirac notation.\]

There are other irreducible representations. For example, ellipsoids can return to the same shape after a pi rotation. This state is \|2,2\>. On the other hand, if the an ellipse is tilted, it will require a full 2\*pi rotation to return to the original position. Such a state would be \|2,1\>.

<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image265.png" style="width:2.83333in;height:2.83333in" alt="A diagram of a mathematical equation AI-generated content may be incorrect." />

Figure 30 - Different m values for spin 2 irrep

It is easy to imagine that we can keep following this procedure to have representations of any integer spin value.

We have thus, almost, arrived at our complete representation of Poincare symmetry for massive objects. We have plane waves valued at each fixed point and fixed momentum with integer spin valued objects representing the internal symmetry of the point.

Before we move on, let’s formalize the generator algebra a bit to better understand how our \|j, m\> state fits into the language of Lie algebra and see what that tells us about allowable values for the spin, j.

Recall where we are, we’ve fixed position and momentum and are exploring the internal rotation symmetry, SO(3) for massive particles. Now, just as our generators for momentum were $`P_{\mu}`$, our generators for rotation are angular momentum generators – $`J_{x},J_{y},J_{z}`$. Now, to make a representation of the rotation symmetry group, we need to find a basis, and to find a basis, we need to find eigenstates of the symmetry generators. But we cannot find eigenstates of $`J_{x},J_{y},J_{z}`$ simultaneously because they do not commute. That is, an eigenvector of one generator is rotated by a different generator. However, we can pick one J component and $`J^{2}`$ which commutes with all of the J components to form a basis without loss of information. A useful way to think of this is that $`J^{2}`$ encodes an overall type of pattern on a unit sphere and the eigenstate of any given J component encodes the variation of the pattern along that axis. To transform to a different J component basis, simply rotate the sphere to have its rotation axis pointing in the direction of the given component. For example, for spin1, the overall pattern is a dipole pattern, while the m value is …. We can see that this is just a basis change from the normal x, y, z Cartesian basis with:\
``` math
\blacksquare( \mid 1,1\rangle\& = 1/\sqrt{}2( - \mathbf{e}\_ x + i"\,"\ \mathbf{e}\_ y),@ \mid 1, - 1\rangle\& = 1/\sqrt{}2(\mathbf{e}\_ x + i"\,"\ \mathbf{e}\_ y),@ \mid 1,0\rangle\& = \mathbf{e}\_ z.)
```

You might wonder – where did the complex coefficients come from. The (j,m) basis is a “complexification” of the x,y,z basis that is needed to express the spherical harmonic representation. Now, using the J eigenbasis approach, we can set up the eigenvalue equation for the generator as we did for momentum and find the solutions. As we saw with momentum, in the wave function representation, the solution are plane waves. Here the solutions will be spherical harmonics, that is, waves on a sphere. These are different from plane waves in that, due to compactness, or periodicity of the sphere, there are boundary conditions that required by waves “fitting on the sphere.” This leads to there being only discreet values for spin. We can think of the spin value (or more accurately the eigenvalue of $`J^{2}`$, which can be shown using classical spherical harmonics, to be j(j + 1)) as being the equivalent of the mass shell for plane wave solutions to the translational symmetry eigenvalue equation. $`J`$, or spin, labels and intrinsic property of the field value just as mass labels and intrinsic property of a wave packet on the field, while m measures the allowed harmonics for objects with a given spin, as k measures the allowed wave numbers for a given mass shell.\
\
With all this in mind, let’s set up the eigenvalue equation for spin:

Pick some axis $`\widehat{n}`$. The rotation group (whether you think SO(3) or SU(2)) has a one-parameter subgroup of rotations around that axis:

``` math
U(\theta) = e^{- \text{ }i\text{ }\theta\text{ }\widehat{n} \cdot \mathbf{J}}.
```

Here:

- $`\mathbf{J} = \left( J_{x},J_{y},J_{z} \right)`$are the generators.

- $`\widehat{n} \cdot \mathbf{J}`$is the generator for rotations about that axis.

- $`J^{2} = J_{x}^{2} + J_{y}^{2} + J_{z}^{2}`$with eigenvalue $`j(j + 1)`$, which labels the irrep.

We also know we can diagonalize $`J_{n}: = \widehat{n} \cdot \mathbf{J}`$together with $`J^{2}`$. So we have a basis of states

``` math
J\hat{}2 \mid j,m\rangle = j(j + 1) \mid j,m\rangle,J\_ n \mid j,m\rangle = m"\," \mid j,m\rangle
```

with $`m = - j, - j + 1,\ldots,j`$

Now, if we look at a full 2π rotation around that axis:

``` math
U(2\pi) = e^{- \text{ }i\text{ }2\pi\text{ }J_{n}}.
```

And act on the eigenstate $`\mid j,m\rangle`$:

``` math
U(2\pi) \mid j,m\rangle = e\hat{}( - "\,"\ i"\,"\ 2\pi"\,"\ m)\ "\," \mid j,m\rangle.
```

We have:

``` math
{▭(U(2\pi) \mid j,m\rangle = e\hat{}( - i2\pi m)\ "\,"\  \mid j,m\rangle.)
}
```
From this equation, we notice if m is integer valued, \|j, m\> returns to itself when acted on by one rotation, $`U(2\pi).`$ However, if m is not integer valued, our state can pick up some phase factor when rotated.

Can m be anything other than integer valued? It would be an odd thing that doesn’t return to itself when rotated once around. The answer, as we will now see is that m can also take half integer values, and nothing else. From the equation above, we see that if spin were a half-integer, and object would return to its starting state under a $`4\pi`$ rotation and would pick up a phase factor of -1 under a $`2\pi`$ rotation. We can construct such an object using the a clever visualization, called the Dirac belt trick.

Wikipedia ([Plate trick - Wikipedia](https://en.wikipedia.org/wiki/Plate_trick)) describes the belt trick as follows:

> The same phenomenon can be demonstrated using a leather belt with an ordinary [frame buckle](https://en.wikipedia.org/wiki/Belt_buckle), whose prong serves as a pointer. The end opposite the buckle is clamped so it cannot move. The belt is extended without a twist and the buckle is kept horizontal while being turned clockwise one complete turn (360°), as evidenced by watching the prong. The belt will then appear twisted, and no maneuvering of the buckle that keeps it horizontal and pointed in the same direction can undo the twist. Obviously a 360° turn counterclockwise would undo the twist. The surprise element of the trick is that a second 360° turn in the clockwise direction, while apparently making the belt even more twisted, does allow the belt to be returned to its untwisted state by maneuvering the buckle under the clamped end while always keeping the buckle horizontal and pointed in the same direction.

Below are two equivalent animations of the same arrangement:

<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image266.gif" style="width:5.20764in;height:3.43819in" alt="r/VisualMath - Animations &amp; Figures Explicatory of the So-Called *Dirac&#39;s Belt Trick*" />\
\
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image267.gif" style="width:2.66944in;height:2.66944in" alt="A colorful spiraling lines connected to a cross AI-generated content may be incorrect." />

Figure 31 - Diracs Belt demonstrating Spinors, 2 gifs.

Are there additional spin values other than integer or half integer? The belt trick suggests there are not. Once we do return the object to its starting state, subsequent $`2\pi`$ rotations will simply repeat the pattern. But we can make this more show this more rigorously using topology. If we build the space of rotations using the axis angle representation, that is, each axis in our rotation operator space represents a rotation about a given physical direction and the coordinate along that axis represents the amount of rotation, then our space of rotations is a (solid) ball.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image268.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image269.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image270.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image271.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image272.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image192.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image273.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image274.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image275.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image276.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image277.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image278.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image279.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image280.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image281.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image282.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image283.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image284.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image285.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image286.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image287.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image288.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image289.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image290.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image291.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image192.png)

Figure 32 - SO(3) Rotation Axix/Angle space

Now, we notice that two opposite (antipodal) points on the ball are actually the same point. There apparent difference is just an artifact of our drawing, the way if we cut a cylinder and lay it out flat, we see a path going around the cylinder starting on one edge of our paper and popping out the other, as in the game Asteroids.

<figure>
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image292.gif" style="width:2.08125in;height:2.08125in" alt="Asteroids Game GIFs - Find &amp; Share on GIPHY" />
<figcaption><p>Figure 33 - The game Asteroids showing a cylinder mapped onto a plane</p></figcaption>
</figure>

There is a topological argument that I will skip here as it really requires building intuition using animations and very careful reasoning which shows that for the SO(3) space, there are two (and only two) classes of rotations, those that return to their starting state after $`2\pi`$ rotations and those that pick up a negative sign (which implies that the return to their starting state after a $`4\pi`$ rotation. The same topology-based argument shows that this “defect” in SO(3) that requires two classes of paths (called, FWIW, two “homotopic” classes) does not exist in SU(2), the space of 2x2 orthogonal complex matrices, which is realized geometrically as a 3-sphere in 4d space. Here, every rotation R in SO(3) is mapped to two unitary transformation U and -U, allowing the two homotopic classes in SO(3) to become a single class in SU(2). Thus spin ½ objects, or **spinors**, are represented not as real, 3d vectors, but as 2d complex arrays operated on by 2x2 complex matrices. One can rotate integer spin objects using SU(2) by ignoring the sign, and, interestingly, video game developers do just this for improved performance as rotations are in some sense “easier” in SU(2), but rotating spinors requires SU(2). This has all been just to mention some of the words used to discuss spinors and SU(2). To learn more, see these YouTube videos:

[Dirac's belt trick, Topology, and Spin ½ particles](https://www.youtube.com/watch?v=ACZC_XEyg9U)\
[The Mystery of Spinors](https://www.youtube.com/watch?v=b7OIbMCIfs4)\
[Quaternions and 3d rotation, explained interactively](https://www.youtube.com/watch?v=zjMuIxRvygQ&t=59s)

We have worked out all the above for SO(3), the symmetry group for massive particles. The reasoning is similar for massless particles that live in ISO(2), roughly the same ideas in 2 dimensions.

### Wave Packet Representation of Symmetry

We have discussed how wave the full Poincare symmetry is represented by wave functions in basis of plane waves and the valuation of those waves lives in an isolated position/momentum fixed “internal” rotation symmetry that is represented by spherical harmonic functions in a basis of spin states. Before we leave the topic of categorizing the kind of wavy objects that transform in spacetime, knowing that our representations are waves, we need to visit a new symmetry that applies to waves, the mixing of wave number and position certainty.

#### Heisenberg Symmetry

We have seen wave packets are objects that Poincare (spacetime’s) symmetry acts on. But another symmetry group acts on them as well, called the Heisenberg group. This symmetry says that if you translate each Fourier mode of wave packet in position or in wave number, the wave packet overall shape stays the same. Now, we know this drill, if we say “the same,” we have to define what that means. In this case, it means, intuitively, the overall shape of the wave packet, that is, the envelope shape.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image293.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image294.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image295.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image296.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image297.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image298.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image299.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image300.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image301.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image302.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image303.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image304.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image305.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image306.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image307.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image308.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image309.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image310.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image311.png)

Figure 34 - Heisenberg Actions, translation in x and k preserve the packet (envelope) shape

Quantitatively, the covariance in phase space (the x,p plane) is constant. Covariance is a measure of how statistical random variables vary together and is visualized (in 2 dimensions) as an ellipse over the joint distribution space. In a statistics setting, this is saying that each concentric ellipse is a level set of probability, where the long axis has the greatest variance and the short axis the least. For example, in the diagram below the x = y axis has the greatest variance, meaning that x and y are strongly correlated:

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image312.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image313.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image314.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image315.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image316.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image317.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image318.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image319.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image320.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image321.png)

Figure 35 - Covariance and correlation ellipse in random variable space for a joint distribution

In the case of waves, the ellipse in phase space is not a level set of probability density but of x, k values composing the packet.

Using this language, we can now say that the invariant of the Heisenberg group action is shape of the ellipse in (x, k) space, which. In quantum mechanics, the becomes (x, p), or phase space, the space of all our local knowledge, of coordinates and their generators, and the composition, in fact, is a probability correlation matrix for measuring position and momentum.

#### 

#### Symmetry Representation in Hilbert Space 

We have discussed complex waves as representations of Poincare and Heisenberg symmetry that take vector or spinor values that abide internal rotation symmetry. Let’s now package all these ideas up into one representation space. As we discussed in the Symmetry section, a representation of a symmetry is a linear algebra vector space in which the vectors and matrix operators map faithfully to the symmetry. While spacetime is the stage on which Poincare symmetry plays out, it is not a representation of Poincare symmetry, for the group action cannot operate linearly on points, but only on displacements. On the other hand, we have seen that the operators can act on the class of functions that we think of as wave packets. Thus, a representation of Poincare symmetry is a space *of wave packet functions*, which can be decomposed as complex plane waves. This space is called a “Hilbert space (after the inventor)” or “state space,” and which evaluate to scalars, vectors, or spinors.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image322.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image323.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image324.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image325.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image326.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image327.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image328.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image329.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image330.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image331.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image332.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image333.png)

Figure 36 - Schematic drawing of Hilbert space

Because both Heisenberg operators and Poincare operators acting on all on-shell waves do not change waves’ amplitude, whatever action the operators perform, the resulting vector lies on a sphere of constant amplitude norm. That is, a unitary operator, like the translation operator, $`\mathbb{e}^{a}\frac{\mathbb{d}}{\mathbb{d}x}`$ , acts as a “rotation” in Hilbert space. Just as spatial rotations preserve real radial distance, unitary operations preserve complex norms. In quantum mechanics, we will give an important interpretation to this amplitude that will map it to the idea that the total probability of all events is 1. The constant “radial distance” of the Hilbert “sphere” can, without loss of meaning, be normalized to 1.

Heisenberg group actions on any wave packet in such a space will preserve the invariant of phase space ellipse shape. However, under Poincare actions you cannot “get from” some wave packets to others. Instead, all components must be on the invariant mass shell. Thus, the wave number representation of Hilbert space we construct is as follows: every axis is a plane wave from a given invariant wavenumber shell. Spatial translation and rotation, boosts, and wave-number translation operators all rotate vectors in this space.

We know commutators encode symmetry, and we know that the value of the commutator tells us the “gap” left over when applying generators in order, then applying their inverses. The Heisenberg commutator (stripped of its context in quantum mechanics and presented purely mathematically, which, as far as I can tell is uncommon in the literature) is:\
``` math
{\lbrack x,k\rbrack = \mathbb{i}
}
```
In our case here, we shift the wave packet in position, then shift in wave-number, then shift back in position, then back in wave-number. In phase space the loop returns us to the same position, by definition, and enclose some area. In Hilbert space, the loop fails to close, leaving a small gap. This gap is precisely the value of the commutator times the area the loop encloses in phase space, which corresponds to the phase shift of the component plane waves. That is, the commutator says that bumping position, then wave-number, then in reverse, multiplies the wave by a global phase:

$`\varphi(x) \mapsto \mathbb{e}^{\mathbb{i}A}\varphi(x)`$

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image334.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image335.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image336.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image337.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image338.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image339.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image340.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image341.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image342.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image343.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image344.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image345.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image346.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image347.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image348.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image349.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image350.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image351.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image352.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image353.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image354.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image355.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image356.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image357.png)

Figure 37 - A loop in phase space induces a phase shift in Hilbert space

#### Uncertainty and operator relations from Heisenberg Commutator

Later, we talk about “gauge theories” in more depth, but we are seeing one here. While the global phase of a wave doesn’t change the wave packet properties, the change in global phase as you move around a loop in phase space implies a “curvature” of the Hilbert space over phase space. The standard terminology is that the base space of phase space with a copy of Hilbert space at each point is a “fiber bundle,” and the curvature is the geometric manifestation of the commutator value.

From this picture, we can find several results that presage the key axioms of quantum mechanics. First, we can formalize where the phase change going around a phase space (the two usages of phase have nothing to do with each other) loop comes from:\
\
Define the unitary “translations” generated by $`\widehat{x}`$and $`\widehat{k}`$:

``` math
U(a) = e^{ia\widehat{k}},V(b) = e^{ib\widehat{x}}.
```

We’ll skip the math here other than to say it uses the same identities we say when discussing Lie algebra and exponential maps, and using: $`\left\lbrack \widehat{x},\widehat{k} \right\rbrack = \mathbb{i}`$ , we can calculate:

``` math
U(a)V(b) = e^{ia\widehat{k}}e^{ib\widehat{x}} = e^{ib\widehat{x}}e^{ia\widehat{k}}e^{iab} = e^{iab}\text{ }V(b)U(a).
```

That is, translating by $`b`$ in $`x`$ then by $`a`$ in $`k`$ differs from doing them in the opposite order by a global phase $`e^{iab}`$.

Next, we can define curvature on the fiber bundle as follow:\
The phase you get by going around a **tiny rectangle** of sides $`\Delta x,\Delta k`$is

``` math
\delta\phi \approx \iint_{\text{rect}}^{}F
```

where $`F = dA`$ is the curvature.

Using the relation above for unitary x and k transformations, we have that the phase from the small loop “$`+ \Delta x`$ in $`x`$, $`+ \Delta k`$ in $`k`$, then back” is

``` math
\delta\phi = \Delta x\text{ }\Delta k
```

Thus, the curvature is given by the infinitesimal loop area:

``` math
\delta\phi = \ F = \mathbf{1}\ dA = \mathbf{1}\ dx \land dk
```

I have bolded **1** to accentuate that the curvature is some factor times the infinitesimal area. For our case of pure, geometric waves that factor is unitless **1** just as the commutator value was unitless **i**.\
\
We can also show with plug and chug algebra that, given, $`\lbrack x,k\rbrack = i`$

``` math
\widehat{x} = x\ \ and\ \widehat{\ k} = - \mathbb{i}\frac{\mathbb{d}}{\mathbb{d}x}
```

Finally, using a version of the triangle inequality for self-adjoint operators:

ΔAΔB≥ ½ ​​⟨\[A,B\]⟩​.

We immediately seetat that:

ΔxΔk ≥ ½\<\|\[x,k\]\| = ½

These relations are all unitless and have no notion of physical size. But if we were to assign a scale factor with dimensions to the commutator, that is:

``` math
\widehat{p} = \hslash\widehat{b} \Rightarrow \left\lbrack \widehat{x},\widehat{p} \right\rbrack = - \mathbb{i}\hslash
```

then we would pressage one of the fundamental results of quantum mechanics:

ΔxΔp \>= $`\frac{\hslash}{2}`$ the Heisenberg uncertainty principle.

#### Boosts and uncertainty

Let’s try to make a more intuitive argument for this uncertainty relation. So far, we have talked about the action of position and wave-number translation in the Heisenberg symmetry group. But our Hilbert space doubles as a representation of Poincare symmetry. We know what translations do already, and rotations operate independently of Heisenberg actions. But we must ask what the actual evolution of a, say free wave, to the phase space ellipse. In this case (x, k) -\> (x + k/m t, k). This has the effect not merely of translating the phase space ellipse by x or k, but of shearing it. Thus, while the exact shape of the phase space ellipse associated with a wave packet does change, the volume it contains does not. What is this saying? It is saying that the “incompressibility” of uncertainty in x, k space (which is familiar to everyone from music, in which drums claps are isolated in time while tuning forks are isolated in pitch) is represented as the incompressibility of the wave packed ellipse as it evolves in phase space.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image358.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image359.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image360.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image361.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image362.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image363.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image364.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image365.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image366.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image367.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image368.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image12.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image369.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image370.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image371.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image372.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image373.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image374.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image375.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image376.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image377.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image378.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image379.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image380.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image381.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image382.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image383.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image384.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image12.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image385.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image386.png)

Figure 38 - Lorentz boosts acting on wave packet preserve phase space area

The term “incompressibility” here is purposely intended to borrow from the idea of an “incompressible fluid” in fluid mechanics as the math is indeed identical. Specifically, we have the identity that no matter how boosts act on the wave:

``` math
\sigma_{x}\sigma_{k} \geq \frac{1}{2}
```

Again, motivating the Heisenberg uncertainty relation $`\Delta x \times \Delta k = \frac{\hslash}{2}`$ .

The same idea is used “Liouville’s theorem” which deals with an ensemble of particles rather than waves and says that the phase space volume taken up by an ensemble of particles in a conservative system remains constant however the ensemble evolves.

#### \
Wave representation summary

Let’s back up and ask what we’ve done here. We’ve said that we can construct a space of wave packet like functions, and we can view that space from multiple useful perspectives. We can simply think of it as a space of waves. We know from common knowledge that waves cannot have an exact position and wave number simultaneously. Alternatively, we can define commutators, derive relations from them algebraically, and rediscover properties we expect from waves. Equivalently, we can think in terms of the geometry of the fiber bundle space and derive the same physical wave-like qualities geometrically. It would be extremely fair to ask, “this is a lot of abstract math, are we just using ever more esoteric ways to describe waves?” There are a couple good answers to that. First, the mathematical, symmetry-based definitions afford different realizations than just what we commonly think of as waves. Secondly, if we want to do calculations, we must have a mathematically formalism to do them in. That said, if you walk away from this discussion thinking “ok, I get spacetime symmetries, and then there’s a bunch of math to describe how waves transform on that symmetry,” that’s a pretty good synopsis.

We’ve also created a taxonomy of wave functions. There are some on this mass shell, some on that. Some that are vector valued, some that are spinor valued. But what is this menagerie of wave packets? Mathematically, they could, for the most part, be just any waves, like those on a pond. But physically, they are not ordinary at all because, for one thing, they are not in any medium. Right now, we simply have no interpretation for them. But, as you probably have guessed, we sprinkle magic reality dust on them by way of quantum mechanics, and, in so doing, we will say that the are the substrate of all energy and matter. And when we say that, we will have that the substrate of matter is the most basic elements we could find that realize the symmetries we live in.

# Quantum Mechanics

We have an understanding of wave function state space, but we’re not sure what to make of the waves. What we do know is that they transform coherently under Poincare symmetry. Quantum Mechanics provides an interpretation of this space of waves. It uses a mathematical framework that was in plain sight to predict results that no one saw coming.

## Seminal Quantum Mechanics Experiments

Let’s look at several experiments that, together, provide the motivation for quantum mechanics.

### Photoelectric Effect, Waves are Particles

Our understanding of the behavior of light and electromagnetism had been built on the understanding of light as waves of energy. An implication of light as a wave is that the energy delivered by a wave should be proportional to its intensity, and the total energy delivered should be the product of intensity and duration of exposure. Contrary to this notion, the “photoelectric” effect is the phenomenon of light absorption providing sufficient energy to dislodge electrons.

<figure>
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image387.png" style="width:2.60764in;height:2.60764in" alt="A diagram of a cell AI-generated content may be incorrect." />
<figcaption><p>Figure 39 - Visualization of Photoelectric Effect</p></figcaption>
</figure>

In the classical wave picture, an electron would absorb enough energy to dislodge after a wave of a given intensity had time to deliver sufficient energy. But observation shows this is not the case. Instead, light with an insufficiently high frequency (color) will *never* dislodge any electrons, no matter the intensity. Instead, light of sufficient frequency will dislodge an electron no matter the intensity of the light. The intensity will only change the rate at which electrons are dislodged. One can “turn down the dial” sufficiently such that only one electron is released at a time, revealing the quantum, or particle-like behavior of waves.\
\
The energy needed to dislodge an electron is given by the famous equation below, which was the first introduction of Plank’s constant, the signature of Quantum Mechanics:\
\
$`E = h\nu`$ , where $`\nu`$ is the frequency of light

### Double Slit Experiment, Particles are Waves

In the famous double-slit experiment, firing a light (or matter) beam through two slits produces an interference pattern associated with waves on a detection screen.

<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image388.png" style="width:3.43819in;height:1.71528in" alt="A close-up of a device AI-generated content may be incorrect." />

<figure>
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image389.jpeg" style="width:3.43819in;height:0.94583in" alt="A blurry green light AI-generated content may be incorrect." />
<figcaption><p>Figure 40 - Setup for and Example Results from double Slit Experiment (<a href="https://en.wikipedia.org/wiki/Double-slit_experiment">https://en.wikipedia.org/wiki/Double-slit_experiment</a>)</p></figcaption>
</figure>

Before we interpret the double slit experiment, let’s discuss the simpler single slit experiment. Like the double slit interference pattern, the single slit shows a wave-like diffraction pattern:\
\
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image390.jpeg" style="width:3.55385in;height:2.00833in" alt="A red and black image of a red light AI-generated content may be incorrect." />

Figure 41 - Single slit diffraction Pattern

If classical particles were passing through the slit, such a pattern would be impossible and we would see a patch on the screen proportional to the slit width rather than a diffraction pattern.

This behavior is of course consistent with the picture of light as a wave. However, if we make the light source sufficiently dim, we can see spots accumulate one at a time on the detection screen. This is obviously something that particles, and not waves, would do.

<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image391.gif" style="width:3.43819in;height:1.53819in" alt="Dots slowly filling an interference pattern." />

Figure 42 - Interference Pattern Appearing one Quantum at a Time

While this phenomenon occurs in the single-slit case, it carries an additional significance for the double-slit case which is that single particle is interfering *with itself*. The picture we have is that the quantum impinging on the slits was a plane wave and the ensuing waves emanating from the two slits interfere depending on the space between the slits, as seen in the illustration below.

<figure>
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image392.png" style="width:2.60764in;height:1.38472in" alt="A grey and white circular pattern AI-generated content may be incorrect." />
<figcaption><p>Figure 43 - Interference Pattern Arising in Relation to Slit Spacing</p></figcaption>
</figure>

As if this weren’t startling enough, we also observe that if we add a detector at either of the slits, the interference pattern disappears and particles hit the screen in two patches that one would expect of particles. This behavior is the physical manifestation of the forthcoming postulate of “wave collapse,” the idea that any measurement results in what *had been* a composite wave packet collapsing into one of its components.

### Stern Gerlach, Spin Showing Superposition and Measurement Basis

The double slit experiment showed that we can think of an object as a wave or particle depending on how we look at it. The more general version of this idea is that a system exists in a “superposition” (linear sum) of states until it is measured. The Stern Gerlach experiment measures spin (the same spin we have discussed) by measuring the angular momentum \[note: we never said spin equates to actual angular momentum, we should add that to classical section\] it carries that can be seen by deflecting a particle with spin in a magnetic field.

<figure>
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image393.png" style="width:3.27569in;height:2.30501in" alt="A diagram of a white rectangular object with blue lines AI-generated content may be incorrect." />
<figcaption><p>Figure 44 - <strong>Stern–Gerlach experiment</strong>: Silver atoms travelling through an inhomogeneous magnetic field, and being deflected up or down depending on their spin; (1) furnace, (2) beam of silver atoms, (3) inhomogeneous magnetic field, (4) classically expected result, (5) observed result</p></figcaption>
</figure>

When this experiment is performed, 50% of particles are deflected “up” by a fixed amount while 50% are deflected “down.” For a spinning object or any classical composition of angular momenta, we would expect that the rotation to be in any direction with an associated continuous spread of deflection amounts.

Now, if we measure a particle in the same way after it has exited the apparatus, we will get the same value we first measured. This is “wave collapse” again – once we measure a certain state, the system is compelled into that state. Recalling from our discussion of spin that up and down are eigenvalues, \[note: we actually didn’t say that, we need to add it\] this result then is telling us something that wasn’t as obvious in the double slit experiment. The distribution function collapses to an eigenstate of the system.

Let’s say we have particles prepared so that they are all “spin up,” and we rotate our measuring apparatus 90 degrees, what do we expect to see? In a classical system, we would expect that the particle to not be deflected at all. But the actual result we get is that the particle is observed “left” and “right” 50% of the time. If we now rotate back to the original orientation without intervening measurements, all the particles will be “up” again. But if, after the left/right measurement, we give only the right-moving particles a small internal twist—a shift in their phase that leaves their angular momentum untouched—something new happens. Nothing changes while we keep looking left/right, but when we turn the apparatus back to the original up/down direction the beams recombine, and that hidden phase matters. The result is no longer all “up.” It becomes 50/50 again.\
Beyond demonstrating that spin must assume one of it’s eigenvalues, the experiment shows two things:

1.  The values you measure are determined by the components in that basis.

2.  There is wave-like (phase) structure that is implied by the correlations between different bases.

Entanglement and Bell’s Theorem\
The following are presented schematically as thought experiments, but they have been performed in a variety of settings.

Two particles can be prepared in a single joint state whose properties cannot be assigned to either particle alone. A familiar example is a pair with total spin zero: if one is “up,” the other must be “down,” and vice versa. The state that captures this is not a choice between the two possibilities but a superposition of both. If we now move the particles far apart and make sure that no signal could pass between them, the correlation still holds. On his own, Bob sees a random sequence—up half the time, down half the time. But the moment Alice measures hers to be up, Bob’s next measurement will also be up with certainty.

So far one might imagine that the two particles carried matching “instructions” from the start, written into them when they were created. But a series of experiments—most famously the Bell tests, recognized with the 2022 Nobel—show this cannot be so. When Alice and Bob are free to choose different measurement directions, the pattern of correlations they see cannot be produced by any catalogue of preassigned values. The statistics violate the very Venn-diagram logic that any “preprepared” story would require.

What remains is the picture quantum mechanics insists on: the pair share a single state whose information is spread across space, whose outcomes are definite only when measured, and whose correlations cannot be reduced to local pieces. It is the natural extension of superposition itself, carried now across distance.

\
Dirac Notation
--------------

We need to take a brief divergence, before discussing the postulates of quantum mechanics, to introduce Dirac notation. This is a way to write matrices and vectors that streamlines the presentation of quantum mechanics theory, and everyone agrees it is easier to teach it than to slog working out an alternate notation that no one uses.

It's not quite fair to say Dirac notation is matrices and vectors. There are a couple of justifications for a new notation aside from convenience. First, because non-commuting observables (operators) cannot be simultaneously expressed (such as in the case of spin directions), there is a need to have a way to signify the higher-level object, the common reality that shows up as different distributions in different bases. Second, because the vectors are generally vectors *of infinite dimensional combinations of eigenfunctions,* many of the vectors and matrices would require infinite rows and columns.

Dirac notation solves these problems by having a single symbol for the operator, another for the vector, and a mirror image of the vector symbol for the transpose, or complex conjugate.

Let’s build up the notation, step by step.

| \|ψ⟩ | A “ket,” the state of the system. A vector, in the generalized sense of something belonging to a vector space. Will often be represented by a complex valued “L2,” or wave-packet like, function. (Note that a function is an infinite dimensional vector in which each coordinate is an axis and each value at a coordinate is a component.) It is, by construction, the thing itself and not a specific representation. For example, a wave can be represented by amplitude over frequency or amplitude over position. \|ψ⟩ is the wave itself, not specifically $`f(x)`$ or $`f(\omega)`$. |
|----|----|

| ⟨ψ\| | A “bra,” the dual state (complex conjugate row v vector). |
|------|-----------------------------------------------------------|

| ⟨φ\|ψ⟩ | A “bracket” (ha, ha), the inner product (overlap, or similarity, of two states, like a dot product of vectors), i.e, the amplitude of \|ψ⟩ in the \| φ\> direction. |
|----|----|

| Â \|ψ⟩ | Operator Â (matrix, possibly infinite dimensional function operator like d/dx) acting on the state \|ψ⟩, producing some new state. |
|----|----|

| ⟨φ\|Â\|ψ⟩ | The amplitude in the \| φ\> direction after finding Â \|ψ\> |
|-----------|-------------------------------------------------------------|

| \|aᵢ⟩ | Eigenstate of observable Â with eigenvalue aᵢ. This is first time a basis has entered the notation. The set {\|aᵢ⟩} is the basis tied to measuring Â. If \|a\> is a continuous basis (such as position), we omit the subscript. For example, \|x\> is the eigenstate of the operator $`\widehat{X}`$ with the eigenvalue x. |
|----|----|

| Â \|aᵢ⟩ = aᵢ \|aᵢ⟩ | Eigenvalue equation. |
|--------------------|----------------------|

| cᵢ = ⟨aᵢ\|ψ⟩ | Amplitude coefficient for outcome aᵢ. Continuous case: c(a) = ⟨a∣ψ⟩ |
|----|----|

| \|ψ⟩ = Σᵢ cᵢ \|aᵢ⟩ | Expansion of ψ in a basis. Continuous case: \|ψ⟩ = ∫ da c(a) \|a\> |
|----|----|

| ψ(a) := ⟨a\|ψ⟩ | Wavefunction in the Â eigenbasis. |
|----|----|
| Aᵢⱼ := ⟨aᵢ\|Â\|aⱼ⟩ | Matix element of operator Â. Continuous case: A(a,a′) := ⟨a\|Â\|a′⟩ |

| Σᵢ \|aᵢ⟩⟨aᵢ\| = **1** | Completeness. Basis spans the state. |
|-----------------------|--------------------------------------|

| ⟨ψ\|ψ⟩ = 1 | Normalization. Total probability is 1. |
|------------|----------------------------------------|

This notation is elegant, but slippery. Let’s turn to stating the basic postulates of Quantum theory, then we will come back and do a couple of illustrative example to help make the theory and the notation sink in.

## Theory of Quantum Mechanics

The theory of Quantum Mechanics is built from a several core ideas. Let’s examine these.

### State

A single “particle,” or identifiable unit of state, is a vector in an irreducible representation of Poincare symmetry. Recall that Poincare symmetry is the full symmetry group describing spacetime. An irreducible representation of the Poincare group is a space of wave-packet-like functions composed of complex plane waves whose values represent internal symmetries and, as we have seen, can be scalars, vectors, or spinors. We see that an “object,” or “identity” in this view is defined functionally as a “carrier” of the symmetry. There *is no other definition* of “what the thing is.”

A specific state is a single vector in such a Hilbert space. The words “vector” and “state” are both chosen carefully.

Vector spaces are spaces of real things. Their mathematical nature comes from the properties they abide, not in being lists of numbers. The “vectors” that are states are the objects that represent spacetime symmetry. An ordinary wave on a string is a member of a vector space regardless of whether it is written as list of amplitudes vs position or a list of amplitudes vs frequency. Thus, when we say that the state of a system is a vector, we are saying it is a real object that we can add, that is closed under addition, etc., not a thing is a certain list of numbers.

So much for “vector,” why does the theory quantum mechanics stress the word “state”? Belaboring the term “state” may seem academic, but we see that is not when comparing to “classical” state. Classical state means everything we need to know about a system now to predict its future. That state is just the positions and momenta (in the general sense of symmetry parameters and their tangent vectors.) If we understand physics to describe an objects path, it is a mathematical fact that knowing the position and tangent at any point on that path is sufficient to “move the object” to the next point. Thus, at any moment in time, that state for a system system of particles is given by its “initial conditions,” $`\left( \mathbf{x}_{1},\mathbf{x}_{2},\mathbf{x}_{3}\ldots\mathbf{v}_{\mathbf{1}},\mathbf{v}_{\mathbf{2}},\mathbf{v}_{3}\ldots \right)`$.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image394.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image395.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image396.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image397.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image398.png)

Figure 45 - Coordinate and 1st derivative on a curve fully suffice to predict next point

But this is not what is meant by “state” in quantum mechanics. As we will see shortly, there is no notion of exact position and momentum in quantum mechanics, therefore “state” cannot be a set of definite values for each degree of freedom and its tangent. Instead, “state” is a mathematical and physical object from which measurement outcomes can be extracted using some procedure. Notice the subtle ontological shift here. “State” is a real thing, but it is not a thing one can look directly at, but rather a thing one posits that encodes patterns relating measurements.

### Measurements and Representations

In order to talk about measuring some quantity, we describe the state using a set of labels that are the numerical values of that quantity. Again, we can go back to simple waves to ground our intuition. If we want to write down the results of measuring the wave number spectrum of a wave packet, obviously we must express the wave as a function of frequency. We can push this intuition farther. The spectral decomposition of a wave packet, that is $`\psi(k)`$, is the contribution from each plane wave, and the value of $`k`$ is the eigenvalue of the translation generator acting on one of its eigenstates, i.e., on a plane wave. That is, $`- i\frac{\mathbb{d}}{\mathbb{d}x}\mathbb{e}^{\mathbb{i}kx} = k\mathbb{e}^{\mathbb{i}kx}`$. Writing the wave packet as a function of $`k`$ is thus mathematically equivalent to writing the wave packet as a vector in the basis of eigenstates of the translation generator.

### Planks Constant Connects Wave Representations to Physical Quantities

Wave functions are our symmetry representations, and the way you translate a wave function is to advance its phase. (If you this doesn’t ring a bell, just draw a pure sine wave, move the x axis to the left, and observe that phase advances.) Now, we are going to give this wave function a physical meaning, and so, we should expect advancing the phase to have some physical meaning. Just as we gave coordinate and tangent vectors in spacetime physical meaning by giving the cone and mass shell units through the value of c and the mass of an object, so we now map the phase of our representing wave function onto the material world with a constant with units. The translation operator that acts on complex plane waves (a suitable basis for any wave function) is:

``` math
e^{ik_{\mu}x^{\mu}}
```

That is, $`\psi_{(x + a)} = \mathbb{e}^{\mathbb{i}k^{\mu}\left( a^{\mu} \right)}\mathbb{e}^{\mathbb{i}k^{\mu}\left( x^{\mu} \right)} = \ \mathbb{e}^{\mathbb{i}k^{\mu}\left( a^{\mu} + {\ x}^{\mu} \right)}`$. and $`k_{\mu}`$is the eigenvalue of the generator of translations.\
\
We also know from Relativity (for a free classical particle) that:\
$`S = p_{\mu}x^{\mu}`$ = $`m\int\mathbb{d}\tau`$

This equation reminds of that action is the generator of translations summed over the path, in classical phase space $`\left( \mathbf{x}_{1},\mathbf{x}_{2},\mathbf{x}_{3}\ldots\mathbf{p}_{\mathbf{1}},\mathbf{p}_{\mathbf{2}},\mathbf{p}_{3}\ldots \right)`$, $`\oint p\mathbb{d}x`$. It ties symmetry transformations and their generators into a single number that is associated not with a local state but with a path, or “history.”

Going back to the equations above, we can now say that, if we want to give the wave function a physical meaning, with units, we can replace the purely geometrical $`k_{\mu}x^{\mu}`$ as follows:\
``` math
\left\lbrack k_{\mu}x_{\mu} \right\rbrack \rightarrow \left\lbrack \frac{p_{\mu}x_{\mu}}{\hslash} \right\rbrack = \left\lbrack \frac{S}{\hslash} \right\rbrack
```

And, since this shows up as a phase shift in the plane wave being operated on, we have the identity:

``` math
phas\mathbb{e} = \frac{S}{\hslash}
```

Planks constant, $`\hslash`$ = ⁻³⁴ J⋅s. This is obviously incomparably tiny compared to everyday actions, and we might expect that it therefore shows up only at tiny scales, which is exactly correct.

Because the wavefunction represents symmetry through phase, any process that returns a system to an equivalent physical configuration must also return its phase to itself, up to an integer multiple of $`2\pi`$. Since phase is given by:

$`S/\hslash`$

This means that in periodic processes the accumulated action over one cycle must come in steps set by $`h`$. In this sense, Planck’s constant is the unit that converts classical action into quantum phase, and it fixes the scale at which interference and discreteness become unavoidable. When actions are large compared to $`h`$, phase winds many times and quantum structure averages out, but when actions are comparable to $`h`$, phase coherence becomes physically visible. We have hinted that the tininess of the constant tells us something new and unexpected might be happening at small scales. This is a good point to pause and meditate – there is some new, physically real, constant of nature telling us the scale at which nature is inherently “pixelated.”

### The Born rule -- Quantum State Encodes the Probability of Measurements

Up to now, we have discussed how quantum mechanics is connecting the geometry of representations to physical quantities. Now it’s finally time to reveal what this encoding is:

> *The probability distribution over a given observable is given by the square of the state in the representation of that observable. For example, in the position representation for a single dimension, the probability distribution over x is given by:*
>
> ``` math
> P(x) = \left| \Psi(x) \right|^{2}
> ```

Our story to this point, about symmetry representations, state space, choice of eigenbasis, and the role of Plank’s constant in mapping these geometric structures to physical observables is now imparted with a physical meaning by this statement. Does this make sense intuitively? Different physicists and natural philosophers would tell us different things. But we can say this, for better or worse. We have been hinting that thinking in terms of instinctively recognizable rigid objects is putting the cart before the horse, and that we should instead think about what geometric forms are consistent with symmetry. In taking this view, we have opened ourselves up to the possibility that the fundamental nature of the realization of these symmetries could be something unexpected. And, if our certainty that there must be rigid objects with definite positions gives way in some regime, it is perhaps least surprising that the regime is at unimaginably small scales.

#### Wave Collapse

Once a measurement is made, the system continues to evolve as specified by the wavefunction. But, in the description above, we said that a measurement yields a single eigenvalue. We are thus inescapably led to the idea of “wave collapse.” Before a measurement, the wave packet has some typical packet shape over, say, position. But upon measurement, the wave collapses to a single value. Afterward, it may again smear out and take on more of a wave packet shape. Quantum wavefunctions in other respects behave as one would expect waves would, but collapse is entirely unexpected. This is troubling, even today, even to professionals, some of whom find in this a reason to be skeptical of the finality of quantum theory.

#### Quick Examples of the Born Rule

Let’s do a few examples to make this more concrete. Suppose we have a state that is a superposition of definite position values. In the position representation, this means

⟨x\|ψ⟩ = ψ(x) = a ψ(x₁) + b ψ(x₂).

Here the state has support at two distinct position eigenvalues, x₁ and x₂, with complex amplitudes a and b.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image399.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image400.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image401.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image402.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image403.png)

> ![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image65.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image404.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image405.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image406.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image407.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image408.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image409.png)
>
> ![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image410.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image411.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image412.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image413.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image414.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image415.png)

Figure 46 - Components of Wavefunction in position representation

According to the Born rule, the probability distribution over position is given by the squared magnitudes of these coefficients. In this discrete example, we therefore have

P(x₁) = \|a\|²,\
P(x₂) = \|b\|².

This example is useful because the relation between amplitudes and probabilities is completely transparent. More typically, however, a quantum state has support over a continuous range of positions.

\[k\_\mu x\_\mu\] \to \[p\_\mu x\_\mu / \hbar\] = \[S / \hbar\]

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image416.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image417.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image418.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image419.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image420.png)

Figure 47 - Continuous distribution over x

In this case, the wavefunction ψ(x) assigns a complex amplitude to every position x, and the probability density of finding the particle at position x is

P(x) = \|ψ(x)\|².

The same abstract state can just as well be represented in the momentum basis. In that case, the probability density for momentum is given analogously by

P(p) = \|ψ(p)\|².

### Probability Conservation and Real Measurements

Since our state is now a distribution, we have a requirement that the integral (of the square of) that function is always one, ensuring that the total probability is one. When we think of functions as vectors, this amounts to saying that our transformations must be rotations in Hilbert space, for the property of rotations that they preserve angles and distances, in the infinite-dimensional case, manifests as preserving the relationship of the value at each point of the function to the value at every other point. We call this property “unitarity.” We have discussed that transformations are given by exponentiating generators:

``` math
{U(\varepsilon) = e^{- \text{ }\frac{i}{\hslash}G\text{ }\varepsilon}.
}{
Now,\ the\ }
```
requirement that $`U(\varepsilon)`$ is unitary puts a requirement on $`G`$. The condition for unitarity is:\
\
``` math
U^{\dagger}U = I
```

($`U^{\dagger}`$ is the complex equivalent of a matrix transpose). It is just a bit of algebra to then show that this forces the requirement on G that:\
\
``` math
{G^{\dagger} = G
}
```
This property is equivalent to $`G`$ being “real” so that the exponent is purely imaginary, which, as we know, causes pure rotations, and that is just the condition we needed for unitarity. The property $`G^{\dagger} = G`$ is called “Hermetian,” and, omitting the derivation, Hermetian operators always have real eigenvalues. This is a very happy result, for in quantum mechanics measurements are defined to be the eigenvalues of generators, and measurements had better be real!\
\
We can summarize the preceding by saying that in quantum mechanics “evolution is implemented with unitary operators and measurement is implemented with Hermetian operators.”

### Implications of State Being a Wavefunction

We have seen that wavefunctions represent symmetry through phase, and that translation acts on a plane wave by advancing that phase. At the purely geometric level, this is captured by the commutator

\[x, k\] = i,

which encodes the Fourier-dual relationship between position and wave number. Once we introduce physical units through the identification p = ℏk, this same geometric structure becomes the canonical commutator of quantum mechanics,

\[x, p\] = iℏ.

This single relation is the most compact expression of how symmetry, phase, and physical measurement are tied together in the quantum theory.

From the canonical commutator we immediately recover the representation of momentum as the generator of translations. In the position representation this takes the form

p = - iℏ d/dx,

while in the momentum representation the position operator appears as

x = - iℏ d/dp.

This expresses in operator language the same fact we saw geometrically: translation acts by phase advance, and momentum is the rate at which phase turns as we move in space.

Because non-commuting operators cannot be simultaneously sharp, the same commutator also implies the Heisenberg uncertainty principle,

Δx Δp ≥ ℏ / 2.

This is not a statement about experimental clumsiness. It is a direct consequence of the fact that the state is a wave, and that position and momentum are Fourier-dual aspects of that wave. A state localized in position must be spread in momentum, and vice versa.

The same phase structure also explains why energy becomes quantized in periodic systems. In any cyclic process, whether a vibration, an orbit, or a bound mode, the phase of the state must return to itself after one full cycle. This requires the accumulated action over the cycle to advance the phase by an integer multiple of 2π. Since phase is given by S/ℏ, this implies that action in such processes is quantized in units of h = 2πℏ. Energy, being action per unit time for a periodic motion, is therefore quantized as well. This is why one cannot construct an arbitrarily small spring with a continuous spectrum of energies.

At macroscopic scales, actions are always enormous compared to ℏ. The phase then advances through an immense number of cycles, and only the phase modulo 2π matters. In this regime, fine phase information is washed out, interference effects disappear, and classical mechanics emerges as an excellent approximation. At small scales, however, S becomes comparable to ℏ, and phase differences carry observable consequences. Interference is no longer negligible, and the full wave nature of the state becomes experimentally visible.

Finally, returning to the plane-wave form of the state, we see that identifying the phase as S/ℏ and the exponent as k_μ x^μ gives

e^(iS/ℏ) = e^(ik_μ x^μ) ⇒ p_μ = ℏk_μ,

showing that energy and momentum are quantized for exactly the same geometric reason: they are the physical measures of how phase advances in spacetime.

### Time Evolution and the Schoedinger Equation

We have seen that the unitary evolution operator, following the pattern we learned for geometric plane waves, is

``` math
U(\Delta x_{\mu}) = e^{- \text{ }\frac{i}{\hslash}\text{ }P^{\mu}\Delta x_{\mu}}.
```

Taylor-expanding as before gives the differential form

``` math
\mid \psi(x^{\mu} + dx^{\mu})\rangle = \left( 1-\frac{i}{\hslash}\text{ }P^{\mu}dx_{\mu} \right) \mid \psi(x^{\mu})\rangle.
```

This leads to the relativistic wave equation

``` math
\partial_{\mu} \mid \psi\rangle = - \text{ }\frac{i}{\hslash}\text{ }P^{\mu} \mid \psi\rangle.
```

Associating $`\partial_{0} = \partial/\partial t`$and $`P^{0} = H`$, the energy operator, we obtain

``` math
i\hslash\text{ }\frac{\partial}{\partial t} \mid \psi\rangle = H \mid \psi\rangle.
```

This is the famous Schrödinger equation. It is the $`F = ma`$ of quantum mechanics, the differential equation of motion which, together with initial conditions, determines the time evolution of a system.

## Quantum Mechanics Experiments Explained

With our theory now in hand, let’s go back to the experiments we described and see how to think of them in light in quantum mechanics.

### Photoelectric Effect

In the photoelectric effect, the energy of the absorbed photon is determined by the energy difference between electron’s energy levels in an atom. The energy levels are quantized because the electron is bound in the atom. As we discussed earlier, periodic processes force the wavefunction to close on itself and be quantized. Similarly, any bound state -- just as the vibrations on a guitar string must “fit” -- is quantized. It’s worth explicitly dispelling the possible misunderstanding that what is “quantum” in the photoelectric effect is that “light is made of particles” nor that “energy comes in quanta.” When we get there, quantum field theory will expand on this idea of boundedness in a way that *does* explain why light (and matter) are particles, but we are not there yet.

### Double Slit Experiment

The first key to understanding the double slit experiment is that, if we ignore the pixelation on the detector screen, the system behaves just as a wave would. Huygen’s principle (1678!) tells us that a plane wave impinging on a slit will propagate as a spherical wave after the slit, as seen in the diagram below (and earlier in the discussion of the double experimental setup).

<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image421.jpeg" style="width:2.26389in;height:2.41667in" alt="Huygens&#39; Principle" />\
Figure 48 - Huygen's principle

Note that the direction of rays perpendicular to the spherical wave are maximally uncertain, while location of point at the slit is maximally certain. This shows us, again, that the uncertainty principle, $`\Delta \times \Delta_{P} \geq \frac{\hslash}{2}`$, is just the expected behavior of a wave.

On the other hand, the observation that detection spots on the screen are discreet, for example, that if we turn the intensity of the beam down sufficiently, spots appear on the screen on at a time, is telling us what the wave is, that it encodes the probability of a particle appearing in a certain state, or, if you prefer to say it in wave-centric language, the wave collapses to an eigenvalue. We are equating “wave collapse” to “particle behavior” to “measurement” here, which is correct. However, we need to resist a temptation. We are *not* equating collapse to localized position. In the single/double slit experiment, we happen to measure position on the screen. But we could tweak the experiment to instead measure momentum and, if we did so, we would get a precise value for momentum, and we would say “this particle had this momentum,” but we would have no information about the location of the particle.

The interference we observe in the double slit experiment is nothing but wavelike behavior, also understood by Huygen. Anyone who has heard nearby tones beating has observed a variation (slightly of tune rather than out of phase) of this. And the explanation, of course, is simply that wave crests can add (interfere constructively) or cancel (interfere destructively). While this is “nothing new” for waves, this “superposition” is the root of a very far-reaching consequences in quantum mechanics. First, it is this structure in the wave components that leads to correlations between measurements in different bases. We will discuss this more next in interpreting the Stern-Gerlach experiment. Second, it provides the necessary richness to support entanglement, which we will discuss when interpreting the (schematic) entanglement experiment.

The fact that probability wavefunctions interfere and collapse gives rise to the thought-provoking ontological question of how materially real wavefunctions are. If they can be “dismissed” as “a way to produce an algorithm for encoding probabilities that happens to have a good visualization,” it somehow loosens what one has to accept. One still must accept probability and entanglement experimental results, but what leads up to them can be attributed to “who knows,” which seems reasonable given that kludgy wave collapse is part of the wave-is-material ontology. On the other hand, science believes in things due to observing their implications, and the existence of wavefunctions perfectly implies quantum mechanics and its taxonomy of fundamental particles. It seems naively contrived to dismiss their ontological status. You choose.

When a particle is detected at slot A, the interference pattern disappears and a sharp cluster behind *both* slits is observed, as one would expect with particles. This result is telling. First, it shows that the act of measuring changes the state. This is a general statement. The only way a quantum state can change is through interaction with another system, and measurement is one such interaction. Second, because the wavefunction is a single extended object, a measurement at one location necessarily changes the total state, including its structure in other locations. We can treat this situation formally. Before the detector is added, the state is

``` math
\mid \psi_{1}\rangle + \mid \psi_{2}\rangle,
```

a single wave with two coherent components. After the detector couples differently to the two paths, the joint state becomes

``` math
\mid \Psi\rangle = \mid \psi_{1}\rangle \otimes \mid D_{1}\rangle\text{\:\,} + \text{\:\,} \mid \psi_{2}\rangle \otimes \mid D_{2}\rangle.
```

The observed pattern comes from the probability density, which is the magnitude squared of this new state. Expanding it shows a cross-term

``` math
\psi_{1}\psi_{2}^{*}\text{ }\langle D_{1} \mid D_{2}\rangle,
```

plus its complex conjugate. Here $`\psi_{1}\psi_{2\ }^{*}`$is the usual interference factor, and $`\langle D_{1} \mid D_{2}\rangle`$ is the inner product of the detector states — a number telling us how distinguishable the two detector outcomes are. If the two detector states are identical, their inner product is 1; if they are completely different, their inner product is 0. Everything in between measures how much the two distributions of outcomes overlap, which is exactly what we mean by their distinguishability. When the detector fully distinguishes the paths, $`\langle D_{1} \mid D_{2}\rangle = 0`$, the cross-term vanishes, and the interference disappears.

### \
Stern-Gerlach Revisited

Recall that in the Stern-Gerlach experiment, particles (silver atoms) are deflected in non-homogeneous magnetic field exactly as would be predicted for a classically spinning object but that, rather than having a continuous spectrum of deflection depending on the orientation of the axis of rotation, are deflected by a fixed amount “up” or “down.” The first thing to understand about the Stern-Gerlach experiment is that it is introducing no new theoretical elements beyond those contained in the double slit experiment. This is no disappointment. It is precisely seeing the same theoretical elements in a new setting that drives home the generalization of the ideas of state, superposition, representation, and measurement to a structure that is deeper than the waves we see in our mind’s eye.

We can now describe Stern–Gerlach in the same language we have been building.\
The state of one atom lives in a tensor product:

``` math
\mid \Psi\rangle \in \mathcal{H}_{\text{motion}} \otimes \mathcal{H}_{\text{spin}}.
```

The first factor comes from the shape of the wave and carries position/momentum information, while the second factor comes from the wave’s value, whether scalar, vector, or spinor, that carries the internal rotation orientation representation. We can visualize this approximately using the animation below in which the wave form travelling is the $`\mathcal{H}_{\text{motion}}`$ factor while the oscillating arrows are the $`\mathcal{H}_{\text{spin}}`$ factor.

<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image422.gif" style="width:2.59364in;height:2.57639in" />

Figure 49 - The typical E&M wave picture shows an example of the two Hilbert space factors

For a narrow incoming packet, we can compress the first factor to “some wave packet moving through the magnet” and write

``` math
\mid \Psi\rangle = \  \mid \text{packet}\rangle \otimes (a \mid \uparrow_{z}\rangle + b \mid \downarrow_{z}\rangle).
```

Nothing new has happened. We have just made explicit that “where it is” and “how it is internally oriented” are two different factors of one state. Let’s remind ourselves where the discrete spin values come from, for example, for the simplest spin-1 case, which transforms exactly like an ordinary vector under rotations. Fix an axis, say the $`z`$-axis, and consider rotations about that axis. A vector parallel to the axis is unchanged by such rotations. Vectors perpendicular to the axis, however, rotate in the plane. When described in terms of their behavior under rotation rather than by fixed $`x`$and $`y`$components, that plane decomposes into two distinct circular behaviors: one that rotates with the frame and one that rotates against it. These three qualitatively different transformation behaviors — unchanged, rotating one way, or rotating the opposite way — are what appear as the three discrete spin-1 values measured along the chosen axis. The discreteness comes not from spatial orientation, but from the requirement that the state transform in a simple, non-mixing way under the symmetry.

We already know how quantum mechanics relates a symmetry to an observable – a Hermitian operator generates a unitary transformation. For spatial motion, translations in $`x`$ give us the momentum operator $`{\widehat{p}}_{x}`$. For spin, rotations about the $`z`$ axis give us the operator $`{\widehat{S}}_{z}`$. Measuring $`S_{z}`$ is a matter of asking which eigenstate of that generator the spin factor is in.

A Stern–Gerlach magnet aligned along some direction $`\widehat{n}`$ is a device that couples the atom’s motion to the generator $`S_{\widehat{n}}`$. Rotate the magnet and you have literally rotated the generator, and with it the preferred basis, as measurement is projection onto eigenstates of whichever generator we chose to wire the apparatus to.

A beam prepared as $`\mid \uparrow_{z}\rangle`$ will always measure “up” if you immediately measure $`S_{z}`$ again. But rotate the magnet to measure $`S_{x}`$instead, and the same state must first be rewritten in the new basis,

``` math
\mid \uparrow_{z}\rangle = \frac{1}{\sqrt{2}}( \mid \uparrow_{x}\rangle + \mid \downarrow_{x}\rangle),
```

so the outcomes split 50–50. Select the “up” branch and rotate the magnet back to $`z`$; the state must be rewritten again,

``` math
\mid \uparrow_{x}\rangle = \frac{1}{\sqrt{2}}( \mid \uparrow_{z}\rangle + \mid \downarrow_{z}\rangle),
```

and the final $`S_{z}`$measurement once more splits 50–50. The incompatibility of the generators is what destroys the original definiteness.

The same point appears even more sharply if we introduce a relative phase. Start with a superposition in the $`z`$-basis,

``` math
\mid \chi(\phi)\rangle = \frac{1}{\sqrt{2}}( \mid \uparrow_{z}\rangle + e^{i\phi} \mid \downarrow_{z}\rangle),
```

and imagine a device that adds a phase $`e^{i\phi}`$to the “down” component. A measurement of $`S_{z}`$is unaffected, because the probabilities depend only on magnitudes. But rewrite the state in the $`x`$-basis,

``` math
\mid \chi(\phi)\rangle = \frac{1}{2}(1 + e^{i\phi}) \mid \uparrow_{x}\rangle + \frac{1}{2}(1 - e^{i\phi}) \mid \downarrow_{x}\rangle,
```

and the phase now changes the actual counting rates:

``` math
P( \uparrow_{x}) = \frac{1}{2}(1 + \cos\phi),P( \downarrow_{x}) = \frac{1}{2}(1 - \cos\phi).
```

A “hidden” phase in one basis becomes a visible imbalance in another.

Let’s examine this situation in the compact language of commutators. The triple $`\left( S_{x},S_{y},S_{z} \right)`$ plays for rotations the role that $`\left( x,p \right)`$ played for motion along a line. Each component is both a generator and an observable, and they fail to commute in a structured way,

``` math
\lbrack S_{x},S_{y}\rbrack = i\hslash S_{z},
```

and cyclic permutations.

This is not an extra rule for spin. It is the same structure we met for motion, where translations were generated by $`p`$ and the mismatch between “shift then measure” and “measure then shift” produced the commutator $`\lbrack x,p\rbrack = i\hslash`$. The resemblance is not cosmetic. Both forms arise from a single fact. A symmetry transformation is implemented by a unitary exponential $`U = e^{- \text{ }iG\varepsilon/\hslash}`$. The same $`\hslash`$ that turns a generator into a phase advance under a small symmetry step also appears in the algebra that records how two such steps fail to commute. Changing from spatial symmetries to rotational ones does not change the rule; only the generators change. In Stern–Gerlach, this algebraic structure stops being abstract and leaves fingerprints in the pattern of spots you record when you rotate the magnets and ask incompatible questions in sequence.

The tensor product makes the basis choices clean. For the motion factor you can choose a basis built from position eigenstates $`\mid x\rangle`$ or from momentum eigenstates $`\mid p\rangle`$. For the spin factor you can choose the $`\mid \uparrow_{z}\rangle, \mid \downarrow_{z}\rangle`$basis or the $`\mid \uparrow_{x}\rangle, \mid \downarrow_{x}\rangle`$ basis, and so on. In each factor the generators are incompatible, and you must choose which one sets the basis. Choosing a generator means writing the state in the basis of its eigenstates, where an eigenstate occupies a single component rather than being spread across several. There cannot be a state that is simultaneously a sharp eigenstate of $`x`$ and $`p`$, nor a state that is simultaneously a sharp eigenstate of $`S_{x}`$, $`S_{y}`$, and $`S_{z}`$. Once one sets up an experiment to measure the value of a generator, the measurement dutifully returns one of its eigenvalues.

Inside the spin factor, the state is described by a pair of complex numbers $`\left( a,b \right)`$. As in the double slit, overall normalization and a common phase do not matter. Only relative phase matters. We can write:

``` math
\mid \chi\rangle = \mid \uparrow_{z}\rangle + e^{i\phi} \mid \downarrow_{z}\rangle.
```

The angle $`\phi`$is invisible if you only ever measure $`S_{z}`$and just count “up” and “down”. It becomes physical when you change basis. Pass the beam through a rotated Stern–Gerlach setup and recombine it and that relative phase shows up as different up/down counts along the new axis. Interference has moved from the screen to the statistics of spin outcomes, but it is the same interference of complex amplitudes.

Line the two experiments up side-by-side and the correspondences almost write themselves. In the double slit the state has two path components. One wave through slit 1, one through slit 2.

``` math
\mid \psi\rangle = \mid \text{through 1}\rangle + e^{i\phi} \mid \text{through 2}\rangle.
```

The observable is position on the screen. The probability pattern comes from the relative phase between the two path amplitudes, read out in the $`\mid x\rangle`$ basis.

In Stern–Gerlach the state has two spin components. One “up” and one “down” along some axis.

``` math
\mid \Psi\rangle \approx \mid \text{packet}\rangle \otimes ( \mid \uparrow_{z}\rangle + e^{i\phi} \mid \downarrow_{z}\rangle).
```

The observable is the spin component along the chosen axis. The probabilities for “up” and “down” along a *different* axis come from the same relative phase, read out in a rotated spin basis.

The correspondences are direct.

- two paths through space ↔ two spin orientations in the internal space

- screen position distribution ↔ up / down spot distribution

- phase between $`\psi_{1}`$and $`\psi_{2}`$↔ phase between the two spin components

- changing from $`p`$ to $`x`$to see fringes ↔ changing from $`S_{z}`$to $`S_{x}`$or $`S_{y}`$to see spin “fringes” in the counts

The algebra — the pattern of generators, commutators, and eigenstates — under both is the same. A state is a vector. Symmetry gives us unitary transformations and Hermitian generators. Non-commuting generators force us to choose a basis. Complex amplitudes carry relative phase that only becomes visible when we ask the question in a different basis.

Stern–Gerlach is the double slit for an internal degree of freedom. That is the point. Not a new trick, but a confirmation that the structure we have built is not about waves on a screen. It is about how any quantum degree of freedom behaves once symmetry is written in complex-valued representations.

### Entanglement and Bell’s Theorem Revisited

We introduced a schematic experiment in which space separated, correlated spin particles are compelled to preserve that correlation when either location is measured. In the case of perfect anti-correlation

``` math
\frac{1}{\sqrt{2}}( \mid \uparrow \downarrow \rangle - \mid \downarrow \uparrow \rangle)
```

if location A measures spin up, location B will be “forced” to measure spin down. We indicated that an additional experimental setup could demonstrate that it is impossible for there to be some hidden instructions beforehand ensuring this correlation. (We left out the details of this additional experiment for the simple reason that setting up the experiment involves as much calculational care as interpreting the result. We will do both here.)

There are two essential concepts in play here, and we will do ourselves a service to be clear on the roles they play. The first is *superposition*. This is implicit in our understanding of state as a vector in a Hilbert space – the state is a superposition of components. This seems unremarkable in and of itself, but when we recall that each of those components is a *physical outcome*, that is, that the state is *multiple outcomes at once*, we see the paradoxical nature of superposition. Bell’s experiment serves both to clarify exactly what we mean by this statement and to demonstrate that we cannot escape its most jarring implications. The second concept is *entanglement*, which is the notion that in multi-particle systems, there are correlation states that cannot be expressed a combination of individual states. Entanglement allows the most ironclad demonstration of superposition, as we will see, by exploiting spacelike separated correlations to rule out ways to “get around” the paradoxical implications of superposition.

#### Entanglement

From a mathematical perspective, entangled states are simpler than classical probably distributions, as the latter is a particular subspace of the former.

In classical probability, the state of a system is given by a distribution over a set of possible outcomes. For example, for a single spin measured along a fixed axis, the outcomes are “up” or “down.” More generally, a probability distribution can be represented as a function on an outcome space, normalized so that its total weight is one.

Mathematically, these functions naturally live in an $`L^{2}`$ space, that is the space of square-integrable functions equipped with an inner product. This structure is central to probability and statistics — variance, covariance, correlation — are all inner-product statements in disguise. Such functions naturally carry unitary representation. They are, in essence, the mathematical definition of what we have been referring loosely to as “wave-packets” or wavefunctions. What classical theory *does not* allow is arbitrary superposition of such wave-packets as new physical states.

When we consider joint systems, classical probability constructs them using a product structure. If Alice’s system has outcome space $`X`$ and Bob’s has outcome space $`Y`$, then the joint system is described on the product space $`X \times Y`$. At the level of functions, this corresponds to a tensor product: joint distributions live in a space naturally identified with $`L^{2}(X) \otimes L^{2}(Y)`$, or equivalently $`L^{2}(X \times Y)`$.

However classical joint distributions do not fill this tensor product space but live on a “simplex” inside the full space that can be written in terms of weighted combinations of definite outcomes.

<figure>
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image423.png" style="width:3.31073in;height:2.34722in" alt="Probability Simplex" />
<figcaption><p>Figure 50 - Probability simplex</p></figcaption>
</figure>

Entangled states are simply all the states in the full tensor product space that are not on the simplex, that is, that cannot be written as weighted combinations of the outcomes of each separate random variable.

Living on the simplex carries the core assumptions of classical physics: that systems possess definite properties, that uncertainty reflects ignorance about which definite state one obtains, and that correlations arise only through mixing pre-existing possibilities. Entangled states that live off the simplex flout these assumptions.

Imagine we had a state for a two-coin system,

``` math
\mid H_{1}H_{2}\rangle + \mid T_{1}T_{2}\rangle,
```

(up to normalization). This state cannot be written as a product of single-coin states such as

``` math
( \mid H_{1}\rangle + \mid T_{1}\rangle) \otimes ( \mid H_{2}\rangle + \mid T_{2}\rangle).
```

We won’t show the proof here, but it is just a few lines of algebra to do so.

More importantly, this state cannot be understood as any mixture of definite joint outcomes. That is, if we insist (as classical probability requires) that every conceivable arrangement of the coins — $`\left( H_{1},H_{2} \right)`$, $`\left( H_{1},T_{2} \right)`$, $`\left( T_{1},H_{2} \right)`$, or $`\left( T_{1},T_{2} \right)`$— corresponds to a definite underlying state, then there is no way to construct a state in which “if we measure heads for coin 1, we will always measure heads for coin 2, and if we measure tails for coin 1, we will always measure tails for coin 2.”

This, then, is the definition of entanglement: a joint state that cannot be factored into individual states. This is doubly confusing in quantum mechanics because each individual state can itself be in a superposition. For example, as we have seen, a single spin can be in a superposition

``` math
\mid \uparrow \rangle + \mid \downarrow \rangle.
```

Thus, even the constituent states of an entangled system do not correspond to definite outcomes, and it is possible to entangle states that are already in superpositions.

Where entanglement drives home the meaning of superposition is this. When looking at a single superposed state such as $`\mid \uparrow \rangle + \mid \downarrow \rangle`$, one might be tempted to interpret it as mere ignorance about whether the spin is up or down. Entangled states, by contrast, demonstrate — without recourse to elaborate “escape hatches,” which we will discuss when treating Bell’s theorem — the logical inconsistency of understanding superposition as nothing more than a statement of ignorance.

As one can see from the diagram of a simplex on tensor product state, there is infinitely more available space in the full product space than on the simplex. This explosion of available states has implications for nature and technology. In nature, entanglement provides a mechanism for increasing entropy, that is for an increased number of possible states. In technology, entanglement is the cornerstone of quantum computing. Whereas a single computation in an n-bit binary computer can move from one $`2^{n}`$ state to another $`2^{n}`$ state, a single computation in a quantum computer can move from a superposition of $`2^{n}\`$states to another configuration of $`2^{n}`$ states. How exactly one extracts useful information out of a superposition is the regime of quantum computing algorithms, and outside our scope.

#### Bell’s Theorem, or the Impossibility of Definite States

When one first hears that clocks slow down when moving, they’re inclined to think this is crazy talk or that there are some things that simply are inaccessible if you are not a mathematical physicist. But when one internalizes that measurements of length are made with measuring sticks, and every observer must be equipped with one, and clocks are composed of more measuring sticks, one can come around to accepting that Relativity, as far-out as it is, is logically plausible. On the other hand, the implication of quantum mechanics – that a state is nothing but a probability distribution of measurements that enforces instantaneous correlations across any distance – feels logically implausible. Or perhaps it would be better to say that we don’t even know how to evaluate its plausibility. We can attempt to explain these implications three ways. The first restores the logical order we expect, but it is demonstrably wrong. The remaining two require us to think differently than we are used to.

1.  Objects actually are in a definite state AND there is no instantaneous communication between them. They only appear to be in a superposition because the theory of quantum mechanics is missing some variable. For example, if two spin particles are emitted, it could be that even though we measure each up or down 50% of the time, there is some extra bit of information we just didn’t know about that says “this one is up, this one is down.

2.  Objects have no definite state before they are measured. All that is existent between measurements is a superposition of possibilities.

3.  Objects are in a definite state, but there is instantaneous communication between them allowing them to conspire when measured.

Bell’s theorem states specifically that the measurements that quantum mechanics predicts (which have been experimentally verified) rule out the possibility of (1), referred to as “local hidden variables.” Let’s see how this works.\
\
The Physical Setup

We begin with a pair of spin-½ particles prepared in the so-called singlet state, that is an entangled state with total spin zero. This state is prepared in the lab with an interaction that conserves angular momentum. This state has one crucial property:

If both particles are measured along the same axis, their results are always opposite. That is, if “Alice” measures “spin up” along some direction, “Bob” – measuring along the same direction – will necessarily obtain “spin down,” and vice versa. This perfect anti-correlation always holds.

After preparation, the particles are separated by a large distance. Alice and Bob are far enough apart that their measurements are spacelike separated, in the technical nomenclature or Relativity. That is, no signal traveling at or below the speed of light can connect one measurement event to the other.

<figure>
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image424.jpeg" style="width:3.95139in;height:1.52202in" alt="Bell&#39;s Theorem (Stanford Encyclopedia ..." />
<figcaption><p>Figure 51 - Schematic of Bell's Theorem Demonstration</p></figcaption>
</figure>

Each experiment proceeds as follows:

> • Alice independently chooses one of several spin measurement directions and records a ↑,↓ result.\
> • Bob independently chooses one of the same set of directions and records his ↑,↓ result.\
> • The choices of measurement direction are made freely and locally at each site.

##### What a Local Hidden-Variable Theory Must Do

Suppose we try to explain the observed correlations using a local hidden-variable theory, that is, some theory in which each particle carries instructions dictating its eventual measurement. “Hidden variable” is the term everyone uses in the literature, but it’s a bit dry to me. We can replace “hidden variable theory” with “theory in which objects have a definite state.” Specifically, when the particle pair is created, it carries with it a complete set of instructions specifying what result will occur for each possible measurement direction. These instructions travel with the particles. Measurement merely reveals the pre-existing answers.

Crucially:

- Alice’s outcome depends only on her particle and her detector setting.

- Bob’s outcome depends only on his particle and his detector setting.

- No influence travels between Alice and Bob at the time of measurement.

Because our setup demands anti-correlation along any shared axis, the instructions must be coordinated. If Alice’s instruction says “up along direction X,” Bob’s instruction must say “down along direction X.”

Now comes the key logical move.

If outcomes are pre-assigned, then all possible measurement results exist simultaneously, whether or not they are actually measured. Each particle pair corresponds to a definite assignment of ↑,↓ outcomes for every detector orientation Alice and Bob might choose.

To make this concrete, suppose Alice can measure spin along three directions, which we’ll label $`A`$, $`B`$, and $`C`$. (The specific angles will matter later, for now they are just three distinct orientations.)

For a given particle pair, Alice’s particle must have a definite answer – either ↑ or ↓ -- for each of these three settings. There are exactly $`2^{3} = 8\`$possible assignments.

| **Label** | **A B C** |
|-----------|-----------|
| E1        | ↑ ↑ ↑     |
| E2        | ↑ ↑ ↓     |
| E3        | ↑ ↓ ↑     |
| E4        | ↑ ↓ ↓     |
| E5        | ↓ ↑ ↑     |
| E6        | ↓ ↑ ↓     |
| E7        | ↓ ↓ ↑     |
| E8        | ↓ ↓ ↓     |

Table 5 - All possible Outcome for 3 Detector Setting, Perfect Anti-Correlation

Bob’s particle carries the opposite instructions, because of the perfect anti-correlation along matching axes. Every local hidden-variable theory must, at minimum, amount to a probability distribution over these eight possibilities.

##### The Set-Theoretic Constraint

Now we ask the simple question, among all particle pairs, how often do certain combinations occur?

For example:

- How often does Alice get ↑ along direction $`A`$ while Bob gets ↑ along direction $`B`$?

- How often does Alice get ↑ along $`A`$ while Bob gets ↑ along $`C`$?

- How often does Alice get ↑ along $`B`$ while Bob gets ↑ along $`C`$?

If outcomes are pre-assigned, these events are subsets of the underlying set of pairs, which implies logical facts about the set relations, one of which can be written schematically as:

``` math
P(A^{+},B^{+}) \leq P(A^{+},C^{+}) + P(B^{+},C^{+}).
```

This inequality is not a physical law – it is purely logic applied to sets. It is brain-dead obvious, but a little slippery to say clearly. Let’s try with an analogy.

Think of one person who, for a given day, has definite answers to three yes/no questions:

- Coffee? (A): yes or no

- Breakfast? (B): yes or no

- Phone? (C): yes or no

Now focus on the set of days for which:

Coffee = yes AND Breakfast = yes

Call this set (Coffee = yes, Breakfast = yes).

For every day in this set, the answer to the third question must be either:

- Phone = yes OR Phone = no.

Thus, every day in the set (Coffee = yes, Breakfast = yes) must belong to one of two disjoint subsets:

- Days with (Coffee = yes, Phone = yes)

- Days with (Breakfast = yes, Phone = no)

There is nowhere else for those days to go.

Therefore:

The number of days with (Coffee = yes AND Breakfast = yes) cannot be greater than the number of days with:

(Coffee = yes AND Phone = yes) + (Breakfast = yes AND Phone = no).

That is:

(Coffee = yes, Breakfast = yes) $`\leq`$ (Coffee = yes, Phone = yes) + (Breakfast = yes, Phone = no)

We can also express this generically as: $`A \cap B \leq B \cap C + A \cap C`$ , where $`\cap`$ means “intersection,” and using this formalism, see the logical tautology with a Venn diagram:

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image425.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image426.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image427.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image428.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image429.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image430.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image431.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image432.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image433.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image434.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image435.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image436.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image437.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image438.png)

Figure 52 - Venn Diagram showing Bell's Inequality

Now, Bell’s argument is simply this:

If measurement outcomes are *pre-assigned* for all settings, then the logic dictates the world must preserve this inequality. However, as we will now see, quantum mechanics predicts correlations that cannot be organized into any such globally consistent table, even though each individual question still has a yes/no answer *when asked*.

##### What Quantum Mechanics Predicts

Quantum mechanics does not assign definite outcomes in advance of measurements. Instead, it assigns a state, as we’ve seen, and the probabilities of outcomes depend on the relationship between the measurement direction and that state.

In a local hidden-variable theory, changing the measurement angle only changes which pre-assigned answers are being sampled, so correlations vary by counting how many instruction tables flip as the angle changes. This produces piecewise-linear dependence on angle. On the other hand, if we take *superposition* seriously, what you measure along a certain direction is the dot product of the state along that direction. This is the familiar relation:

``` math
\widehat{a} \cdot \widehat{b} = \cos\theta
```

We can work this out. Due to the double cover nature of spinors that we have discussed, one full rotation is $`4\pi`$, therefore the projection of a given spin direction is $`\theta`$/2. We will use this, but ultimately the violation of Bell’s inequality would work just as well with spin 1 particles and $`\theta`$ rather than $`\theta`$/2.

Now, let Alice measure spin along axis $`\widehat{a}`$ and let Bob measure spin along axis $`\widehat{b}`$, which is rotated by an angle $`\theta`$relative to $`\widehat{a}`$. Expressing Bob’s spin states along $`\widehat{b}`$ in terms of spin states along $`\widehat{a}`$:

``` math
{\mid \uparrow_{\widehat{b}}\rangle = \cos\left( \frac{\theta}{2} \right) \mid \uparrow_{\widehat{a}}\rangle + \sin\left( \frac{\theta}{2} \right) \mid \downarrow_{\widehat{a}}\rangle,
}{\mid \downarrow_{\widehat{b}}\rangle = - \sin\left( \frac{\theta}{2} \right) \mid \uparrow_{\widehat{a}}\rangle + \cos\left( \frac{\theta}{2} \right) \mid \downarrow_{\widehat{a}}\rangle.
}
```

Rewrite Bob’s post-measurement state $`\mid \downarrow_{\widehat{a}}\rangle`$in terms of the $`\widehat{b}`$basis.

``` math
\mid \downarrow_{\widehat{a}}\rangle = \sin\left( \frac{\theta}{2} \right) \mid \uparrow_{\widehat{b}}\rangle + \cos\left( \frac{\theta}{2} \right) \mid \downarrow_{\widehat{b}}\rangle.
```

This tells us the probability amplitudes for Bob’s possible outcomes when he measures along $`\widehat{b}`$.

- Amplitude for Bob to get **↑** along $`\widehat{b}`$: $`\sin(\theta/2)`$

- Amplitude for Bob to get **↓** along $`\widehat{b}`$: $`\cos(\theta/2)`$

Finally, square to get the probability:\
``` math
{P(\text{Bob ↑} \mid \text{Alice ↑}) = {\sin}^{2}\left( \frac{\theta}{2} \right).
}
{Let’s\ check\ that\ the\ quantum\ prediction\ violates\ Bell’s\ inequality.\ Choose\ 3\ angles:
}{A = 0^{\circ},C = 60^{\circ},B = 120^{\circ}.
}
```

Left side:

``` math
P(A \uparrow ,B \uparrow ) = \frac{1}{2}{\sin}^{2}\left( \frac{120^{\circ}}{2} \right) = \frac{1}{2}{\sin}^{2}(60^{\circ}) = \frac{1}{2} \cdot \frac{3}{4} = \frac{3}{8} = 0.375.
```

Right side:

``` math
P(A \uparrow ,C \uparrow ) = \frac{1}{2}{\sin}^{2}\left( \frac{60^{\circ}}{2} \right) = \frac{1}{2}{\sin}^{2}(30^{\circ}) = \frac{1}{2} \cdot \frac{1}{4} = \frac{1}{8} = 0.125.
```

Same for $`P(C \uparrow ,B \uparrow )`$(also $`60^{\circ}`$):

``` math
P(C \uparrow ,B \uparrow ) = \frac{1}{8} = 0.125.
```

``` math
P(A \uparrow ,C \uparrow ) + P(C \uparrow ,B \uparrow ) = \frac{1}{8} + \frac{1}{8} = \frac{1}{4} = 0.25.
```

Bell’s bookkeeping inequality would require:

``` math
0.375 \leq 0.25
```

which demonstrates the violation and forces us to conclude the particles *cannot have a preexisting definite values.*

Of course, this is all theory, but what about the experiment? There have been many experiments that verify this result, but the collection of experiments widely accepted to be free of any possible loopholes resulted in the Nobel prize in physics in 2022.

## Reflections on Quantum Mechanics and What Comes Next

With Bell’s result in hand, we are forced to accept the hardest-to-accept aspects of quantum mechanics. What we call “physical properties,” such as position, are inherently probability distributions. A system state lives in a superposition of possible measurements. In no sense is it secretly hiding its actual measurement. Because states can be entangled, and entangled states can live in a superposition, superposition does not respect the mechanistic, or local, causality we expect from material things. The state, or wavefunction, while only ever directly visible to us through the probability distributions of the measurements it yields, nonetheless leads to interference and the violation of Bell’s inequality, which attests to its reality. And yet, there is no explanation in the theory why it should collapse upon measurement. While it is endlessly tempting to try to find a “way out” of the implications o quantum mechanics implications, perhaps it is better to try to find a “way out” of our ways of thinking that makes its implications so hard to accept. We should appreciate that nothing in quantum mechanics demand we adopt the belief that “the probability distributions we observe is all there is, there is no underlying more satisfying ontology,” but it does require us to believe that, whatever that underlying ontology may be, it is not one of rigid bodies within definite positions.

Thus far, we have talked about symmetry, spacetime, state, measurement, and Schrödinger’s equation, in which exponentiating an energy function of configuration space generates state change over time. We have discussed constant velocity, which is itself another symmetry. What we have not discussed is actual change, that is, interactions, or force, or non-constant velocity. We will treat dynamism with quantum mechanics, but quantum mechanics has a conceptual flaw we must fix before doing so. The issue is not entanglement as those correlations can arise from events in the past. The deeper problem lies elsewhere. Schrödinger’s equation presumes that there exists a single, global notion of time with respect to which the entire state of a system can be specified and evolved. In other words, it treats the quantum state as something defined on a preferred slice of simultaneity. Relativity tells us that no such preferred slicing of spacetime exists. Different observers disagree on what counts as “space at a given time,” and none is privileged. A theory whose fundamental object is a state evolving in a universal time therefore carries extra structure that relativity explicitly denies. To fix this, we will introduce quantum field theory and use it to treat dynamics. But first, we need to learn about dynamics itself, which relates the curvature of the spaces we inhabit to material flows.

# Change and Curvature

We can feel force. If we hold a magnet, we feel magnetic force. When we feel the ground, we feel gravity, the ground pressing up through our feet. The force we feel, as Newton showed, is equated to acceleration, which spells out a path in position space.

Modern physics has a theory of where these forces come from, namely that forces result from the geometry of the spaces we live in. This sounds terribly abstract, but it becomes somewhat more concrete in the case of gravity, where force is indistinguishable from the effects of following *geodesics*, or “straightest possible paths” in curved spacetime. This equivalence says more than that there are two ways to look at gravity. It does what a theory is supposed to do and makes predictions that the theory it replaces and explains cannot. For example, spacetime curvature predicts that light, though massless, is influenced by gravity, which a theory tying gravity only to mass would not.

Implicit in a geometric view of force is that we model the world with fields that permeate all spacetime. The idea of the world being made of rigid bodies with empty space between them is abandoned as the geometric equations that govern dynamics -- how things change in time – treats geometry in a continuous manner.

Other forces arise from the geometry of more complex spaces, called *fiber bundles*, and visualized as fibers over spacetime that include extra degrees of freedom living at each point. In quantum mechanics, one such degree of freedom is the phase of the complex wavefunction. Such a space can feel abstract and remote, so we will build intuition using more tangible examples. This kind of geometric viewpoint explains Maxwell’s laws of electricity and magnetism, while making predictions that Maxwell’s equations alone could not, for example that charge can be affected even when passing through regions of with no electromagnetic forces.

Because force is something we feel locally, its geometric origin must be expressed in differential form. What matters is the local deviation from straightness, not the global shape of the whole space. Forces do not result from the overall shape of space, but from geometry that is apparent locally, supporting a fully differential description. This theory of spacetime is not an inert backdrop through which matter moves. The differential geometry itself responds to what flows through it.

All fundamental interactions we will discuss are conservative in the sense that there exists a function of field configuration space built from symmetries and their generators that can be extremized to determine physical flows that preserve system invariants. What look like irreversible, disorder-producing forces in everyday life arise from the statistics of many underlying degrees of freedom that themselves obey these conservative laws.

## Symmetry, Parallel Transport, and Extremization

In a generalized sense, fundamental constituents of matter, particles like electrons and photons, always travel is in a “straight” line in full space constructed from the symmetry they represent. To make sense of “felt forces,” we have to be very careful about what spaces we are talking about. If an object is traversing a geodesic in spacetime, it will feel no force. However, if, in following a geodesic through a fiber bundle, it deviates from a spacetime geodesic, it will experience a “felt force.” We will unpack this as we get deeper into this chapter. As alluded to already, we will generalize the idea of “straight” in “flat space” to “straightest possible,” or geodesical, in “curved space.” This is nothing more in essence than the idea that following lines of longitude on earth, or more generally “great circles,” or geodesics, on the surface of a sphere. We want to call such a path “straight” because it is the shortest possible path between two points. This informal definition of “straightest possible” contains two elements that we can use to rigorously define *parallel transport*. The first element is that the space has an invariant structure derived from symmetry that allows an agreed upon definition local definition of length. The second element is that what we intuitively see as “straightest” or “simplest” arises from *extremizing* (often “minimizing”) the integral of the invariant length over a path. We will make the bridge from geometry to physics by taking care to build our invariant structure from physical symmetry. Before we do that, let’s “do a little geometry” to make sure these ideas are well grounded. We will show how minimizing length in flat space defines a straight line and how doing the same on a sphere defines a geodesic.

### Using Extremization to Find Geodesics 

Let’s start with a straight line in flat space.

#### Straight Line in Flat Space\
\
\
\

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image439.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image440.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image441.png)

Figure 53 - Minimizing a curve in the plane

We can write any curve in the (x,y) plane in parametric form

``` math
\lambda \mapsto (x(\lambda),y(\lambda)),
```

with fixed endpoints

``` math
\left( x\left( \lambda_{1} \right),y\left( \lambda_{1} \right) \right) = \left( x_{1},y_{1} \right),\ \ \ \ \ \ (x(\lambda_{2}),y(\lambda_{2})) = (x_{2},y_{2}).
```

The length of such a curve is

``` math
L\lbrack x,y\rbrack = \int_{\lambda_{1}}^{\lambda_{2}}\sqrt{\left( \frac{dx}{d\lambda} \right)^{2} + \left( \frac{dy}{d\lambda} \right)^{2}}\text{ }d\lambda.
```

Define

``` math
\dot{x} = \frac{dx}{d\lambda},\dot{y} = \frac{dy}{d\lambda},\ \ \ \ \ \ R = \sqrt{{\dot{x}}^{\text{ }2} + {\dot{y}}^{\text{ }2}}.
```

Then

``` math
L\lbrack x,y\rbrack = \int_{\lambda_{1}}^{\lambda_{2}}{R\text{ }d\lambda.}
```

Now require that this functional (function of functions) be stationary under small variations of the curve that keep the endpoints fixed.

Let

``` math
x(\lambda) \rightarrow x(\lambda) + \varepsilon\text{ }\eta(\lambda),\ \ \ \ \ y(\lambda) \rightarrow y(\lambda) + \varepsilon\text{ }\xi(\lambda),
```

Here:

- $`\eta(\lambda)`$ and $`\xi(\lambda)`$ are arbitrary test functions that vanishe at the endpoints\
  (so the endpoints stay fixed: $`\eta\left( \lambda_{1} \right) = \eta\left( \lambda_{2} \right) = 0,\ \ \ \ \xi(\lambda_{1}) = \xi(\lambda_{2}) = 0`$)

- $`\varepsilon`$ is an infinitesimal number that controls the size of the change

Then

``` math
\dot{x} \rightarrow \dot{x} + \varepsilon\text{ }\dot{\eta},\dot{y} \rightarrow \dot{y} + \varepsilon\text{ }\dot{\xi}.
```

The varied length is

``` math
L(\varepsilon) = \int_{\lambda_{1}}^{\lambda_{2}}\sqrt{\left( \dot{x} + \varepsilon\dot{\eta})^{2} + (\dot{y} + \varepsilon\dot{\xi})^{2} \right.\ }\text{\:\,}d\lambda.
```

Differentiate with respect to $`\varepsilon`$ and evaluate at $`\varepsilon = 0`$:

``` math
{\frac{dL}{d\varepsilon} \mid}_{\varepsilon = 0} = \int_{\lambda_{1}}^{\lambda_{2}}\frac{\dot{x}\text{ }\dot{\eta} + \dot{y}\text{ }\dot{\xi}}{\sqrt{{\dot{x}}^{\text{ }2} + {\dot{y}}^{\text{ }2}}}\text{\:\,}d\lambda.
```

Stationarity requires

``` math
{{\frac{dL}{d\varepsilon} \mid}_{\varepsilon = 0} = 0.
}
{That\ is:}
```

1.  Take some original test curve and test end-point vanishing functions.

2.  Now L($`\varepsilon)`$ is function of $`\varepsilon`$ only.

3.  Thus, for this test curve, epsilon is 0, and if and only if $`{\frac{dL}{d\varepsilon} \mid}_{\varepsilon = 0} = 0`$, the test path is an extremum (stationary point).

Now integrate this by parts, leading to an integrand containing only $`\eta`$ and $`\xi`$ (not their derivatives) and x, y and their derivatives.

``` math
\int_{\lambda_{1}}^{\lambda_{2}}\frac{\dot{x}\text{ }\dot{\eta}}{R}\text{ }d\lambda = \left\lbrack \frac{\dot{x}}{R}\eta \right\rbrack_{\lambda_{1}}^{\lambda_{2}} - \int_{\lambda_{1}}^{\lambda_{2}}\frac{d}{d\lambda}\left( \frac{\dot{x}}{R} \right)\eta\text{ }d\lambda.
```

The boundary term vanishes because $`\eta(\lambda_{1}) = \eta(\lambda_{2}) = 0`$.

Similarly for $`y`$. Therefore the stationarity condition becomes

``` math
\int_{\lambda_{1}}^{\lambda_{2}}\left\lbrack - \frac{d}{d\lambda}\left( \frac{\dot{x}}{R} \right)\eta - \frac{d}{d\lambda}\left( \frac{\dot{y}}{R} \right)\xi \right\rbrack d\lambda = 0.
```

Because $`\eta\`$and $`\xi`$can be any functions that vanish at the endpoints, the only way the integral can be zero for all such choices is for the coefficients of $`\eta`$and $`\xi`$to vanish pointwise. $`\frac{d}{d\lambda}\left( \frac{\dot{x}}{R} \right) = 0,\ \ \ \ \frac{d}{d\lambda}\left( \frac{\dot{y}}{R} \right) = 0.`$*\*

Define $`A,B`$:

``` math
\frac{\dot{x}}{\sqrt{{\dot{x}}^{\text{ }2} + {\dot{y}}^{\text{ }2}}} = A,\ \ \ \ \frac{\dot{y}}{\sqrt{{\dot{x}}^{\text{ }2} + {\dot{y}}^{\text{ }2}}} = B.
```

Square and add:

``` math
A^{2} + B^{2} = 1.
```

From the first equation,

``` math
\dot{x} = A\sqrt{{\dot{x}}^{\text{ }2} + {\dot{y}}^{\text{ }2}}.
```

This implies that the ratio $`\dot{y}/\dot{x}`$ is constant. Indeed,

``` math
\frac{\dot{y}}{\dot{x}} = \frac{B}{A} = \text{constant}.
```

Therefore both $`\dot{x}`$and $`\dot{y}`$ are constant up to an overall multiplicative factor. Integrating,

``` math
x(\lambda) = a\lambda + b,\ \ \ \ \ \ \ y(\lambda) = c\lambda + d,
```

for constants $`a,b,c,d`$.

The curves that make the length functional stationary are precisely functions of the form:

``` math
(x(\lambda),y(\lambda)) = (a\lambda + b,\text{\:\,}c\lambda + d),
```

which are straight lines.

#### Minimizing Length on Sphere

Let’s sketch how we would modify the procedure above to show that geodesics on a sphere are the shortest possible paths in that space.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image442.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image443.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image444.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image445.png)

Figure 54 - Geodesics on a sphere

The procedure proceeds just as for a line in flat space except that our invariant metric change from:*\*
$`ds^{2} = dx^{2} + dy^{2}`$

to:\
``` math
ds^{2} = R^{2}\left( d\theta^{2}+{\sin}^{2}\theta\text{ }d\phi^{2} \right)
```

After carrying out the procedure, we find that:\
\
``` math
{\ddot{\theta} - \sin{\theta\cos{\theta\text{ }{\dot{\phi}}^{2}}} = 0,\ \ \ \ \ \ \ \ \ddot{\phi} + 2\cot\theta\text{ }\dot{\theta}\text{ }\dot{\phi} = 0
}
{which\ are\ the\ equations\ for\ a\ geodesic\ on\ a\ sphere.\ 
}
```

### From Geometry to Physics

A few observations are evident from this discussion. First, the description of curves in terms parameterized equations and their derivatives is the exact same machinery we use for describing physical trajectories. Second, we see that in flat space “acceleration” (second derivative) is zero, while it is non-zero in curved space. Third, the extremization approach we used is identical to the approach used in “Lagrangian Mechanics.” The path length is equivalent to the “Lagrangian,” the differential equations are equivalent to the “Euler Lagrange” equations, and the invariant distance is equivalent to the invariant Minkowski metric on spacetime.\
\
We can now simply reappropriate this approach to find that a inertial path in spacetime is a straight world line. First, we write down the Lagrangian. For a free particle in spacetime, take the Lagrangian proportional to the invariant interval:

``` math
L = - mc\text{ }\sqrt{- \text{ }\eta_{\mu\nu}\text{ }{\dot{x}}^{\mu}{\dot{x}}^{\nu}}
```

Treat $`x^{\mu}(\tau)`$ as generalized coordinates and apply

``` math
\frac{d}{d\tau}\left( \frac{\partial L}{\partial{\dot{x}}^{\mu}} \right) - \frac{\partial L}{\partial x^{\mu}} = 0.
```

Because $`L`$does not depend explicitly on $`x^{\mu}`$,

``` math
\frac{\partial L}{\partial x^{\mu}} = 0,
```

so we get

``` math
\frac{d}{d\tau}\left( \frac{\partial L}{\partial{\dot{x}}^{\mu}} \right) = 0.
```

Compute the momentum-like term:

``` math
\frac{\partial L}{\partial{\dot{x}}^{\mu}} = \frac{m\text{ }\eta_{\mu\nu}{\dot{x}}^{\nu}}{\sqrt{- \eta_{\alpha\beta}{\dot{x}}^{\alpha}{\dot{x}}^{\beta}}}.
```

With proper time parametrization the denominator is constant, giving

``` math
\frac{d^{2}x^{\mu}}{d\tau^{2}} = 0.
```

This is precisely the statement that in flat spacetime, a free particle follows a straight worldline. We will now see how extending this procedure to curved spacetime leads to General Relativity and its explanation of gravity.

## Gravity and General Relativity

The most famous and elegant theory of a “force” being understood in terms of curvature of a space is Einstein’s theory of General Relativity. All objects are attracted to each other by gravity. Colloquially, we call this the “force of gravity.” And yet, an object in free fall feels no force, no pull, whatsoever. An accelerometer in free fall reads zero. Instead, massive objects cause spacetime itself to deform such that following a geodesic, the “straightest possible” path, leads them toward one another. Thus we see gravity as being a force in one sense – it brings things together, but not in another – there is no measurable acceleration on a free body.

### The Principle of Equivalence

If you are in a sealed elevator, no conceivable experiment will tell you that you are in an external force field. For example, if you throw a ball, it goes perfectly straight. The same goes for every other experiment. The absoluteness of this claim is not for emphasis, it is the phenomenological basis for General Relativity.\
\
If you are in an accelerating elevator away from any massive objects, any experiment you perform will behave as though you were in a gravitational field with an acceleration equal to that of the elevator. Again, the absolutism of the claim is essential.

Taking these experiments together, we see viewing gravity as a traditional force “pulling apples down from Newton’s tree” is precisely reverse.

1)  The apple is not accelerating.

2)  Newton, constrained to the surface of the earth, is accelerating toward the apple.

We are biased against this view as we are conditioned to believe we are at rest when standing on earth, but we already know this is not the case. And we know that any claims we make must be grounded in experiments we can perform. Our elevator experiments above put to rest the idea that the apple could possibly be accelerating and confirm that Newton standing on the surface of the earth (as an example) is accelerating.

So far so good, but this analysis leaves one thing unaccounted for. Why does the apple want to approach the earth if not for a force of attraction. The answer is that spacetime is curved by matter such that the apple is following its “straightest possible,” or “inertial” path, and that path takes it in the direction of earth.\
\
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image446.gif" style="width:4.81892in;height:2.71528in" />

Figure 55 - A Pressurized Earth Accelerates Outward with respect to Spacetime Geodesics

### Einstein Gravitation Field Equation

Einstein’s field equation is:

``` math
G_{\mu\nu} = 8\pi G\text{ }T_{\mu\nu}
```

(Note that we are omitting the $`\Lambda g_{\mu\nu}`$“cosmological constant” term here, which is non-essential for our story.) We can write this equation schematically as:

**Spacetime curvature** ⟷ **Energy distribution**

On the left-hand side is the expression for curvature, $`G_{\mu\nu}`$, a $`4 \times 4`$rank-2 tensor (thus the two indices) describing the curvature of spacetime. On the right side is the expression for matter distribution, $`T_{\mu\nu}`$, another $`4 \times 4`$rank-2 tensor, describing the spacetime flux of 4-momentum, where the first index labels which 4-momentum component and the second index labels which 3-dimension hypersurfaces it flows through.

What are we saying? Start with flat spacetime. Treat it as a canvas. On this canvas you place fields that return numbers about measurement events. The most elemental of these, the “basis field,” is the one that says how measuring sticks and clocks perform. That field is the metric.

``` math
ds^{2} = g_{\mu\nu}\text{ }dx^{\mu}dx^{\nu}
```

Every other field you write down is ultimately described in terms of it, because all such fields rely on some notion of distance, time, and angle.

Now the Einstein field equation claims that the matter field, or more specifically the 4-momentum distribution $`T_{\mu\nu}`$, couples to this basis field. That is, where we have “more mass” we have “greater curvature.” This relationship allows objects to come together by following spacetime geodesics without experiencing any local acceleration. Let’s try to arrive at a sort of mechanical mental model of what the Einstein field equation is saying.

The first observation we make is that both sides of the field equation are divergence-free. That is:

``` math
\nabla_{\mu}G^{\mu\nu} = 0\nabla_{\mu}T^{\mu\nu} = 0
```

On the geometry side this expresses the self-consistency of the bending. That is, it says that our metric field does not discontinuously jump. The vanishing divergence is saying that curvature cannot appear or disappear without regard to its surroundings. On the matter side, the vanishing divergence expresses the local conservation of 4-momentum. It says that if you draw a 4-cube around a distribution, there is no net flux out of the cube. Or, if you separate time and space components, that any flux out of a spatial cube is offset by the rate of change of density.

Our second observation is that setting each side of the field equation on its own to zero has an interpretation. Setting the matter side to zero describes empty space:

``` math
T_{\mu\nu} = 0
```

Setting the curvature side to zero describes spacetime in the absence of matter sources:

``` math
G_{\mu\nu} = 0
```

This does not require spacetime to be globally flat. It says only that curvature is not being directly sourced by matter in that region.

Our third observation is to examine how $`T_{\mu\nu}`$and $`G_{\mu\nu}`$are constructed at a high level. $`G_{\mu\nu}`$is a differential operator built from the metric and its first and second derivatives, plus products that make it nonlinear. Schematically, it is built from:

``` math
G_{\mu\nu} \sim \partial^{2}g_{\mu\nu} + (\partial g_{\alpha\beta})^{2}
```

There is quite a bit of differential geometry machinery one needs to work through to calculate $`G_{\mu\nu}`$, but the important message is this: the curvature $`G_{\mu\nu}`$that accounts for the “apparent force of gravity” is a differential field equation of the metric $`g_{\mu\nu}`$.

On the right is a different kind of object. It packs all the momentum components over spacetime into a stress tensor, a bookkeeping device for energy density, momentum density, pressure, and shear.

``` math
T^{\mu\nu} = \begin{pmatrix}
\text{energy density} & \text{energy flux} \\
\text{momentum density} & \text{stresses}
\end{pmatrix}
```

Engineers will recognize this — it is the same type of object used to calculate the structural integrity of buildings.

Putting all these observations together, we have the following model. The Einstein field equation expresses the coupling of two field equations. One side is governed by a differential equation in the metric, while the other side is a flux equation, which also necessarily includes the metric. One side acts like a deformable sheet upon which 4-momentum flows, while the other side acts like the continuous flow of 4-momentum. The equation tells how the two sides are coupled.

All this sounds believable enough viewed step-by-mathematical-step, but the astounding fact is that this model leads to exotic, testable implications we can now put into context.

### Implications of General Relativity

That gravity is the result of the curvature of spacetime may feel a distant abstraction, but the implications are astounding.

#### Time Dilation

Clocks slow down the closer they are to massive-energetic bodies. We showed earlier, in the “twin paradox,” that non-inertial motion leads to clock slow down. By the equivalence principle, gravitation and acceleration are equivalent, thus we conclude the time must also dilate in a gravitational field. As we showed, the clock of the twin that turns around it “misses events.”

<figure>
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image261.png" style="width:4.41425in;height:3.24684in" alt="A screenshot of a video AI-generated content may be incorrect." />
<figcaption><p>Figure 56 - Rocket twin misses earth twin history</p></figcaption>
</figure>

The same is the case for any non-intertial frame, whether it turns around fully at a vertex or gradually curves. Let’s illustrate the same idea using a different experiment. Bob, in deep space at rest in his frame has a clock. He emits two pulses of light and records the time his watch shows has elapsed between the pulses. Alice is in an accelerating frame when she receives the pulses. To make the comparison of their clocks more clear, we’ll add a third observer “Alice-reference” that takes an inertial path between the two pulse receptions. This simply allows Alice and Alice-reference to meet and compare their clocks, exactly as in the twin paradox. We could have arranged an experiment just as well without Alice-reference, but this setup is a bit easier to arrange. Using the Minkowski distance metric, we see that any non-inertial path’s clock measures less time. Alice ages less than Alice-reference (and, equivalently, Bob). Her clock runs more slowly. This situation is illustrated below.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image447.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image448.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image449.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image450.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image65.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image451.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image452.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image453.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image454.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image455.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image456.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image457.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image458.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image192.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image459.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image460.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image461.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image462.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image463.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image464.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image465.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image466.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image467.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image468.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image469.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image470.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image471.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image192.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image459.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image472.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image473.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image474.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image475.png)

Figure 57 - Alice2's non-inertial clock moves slower (experiences less proper time) then Alice or Bob’s

Now, rather than Bob and Alice in deep space and Alice accelerating, allow Bob and Alice to be in fixed location with respect to a gravitational body in which Bob’s space is nearly flat (farther away from the gravitational source) and Alice’s is more curved (closer to the mass). Both traverse paths that look straight and change in time only with respect to the reference base flat spacetime against which we measure curvature. But now Bob is on his spacetime geodesic while Alice is off it. Since Alice is off the geodesic, her proper time is less, she ages less, exactly as in the accelerating case.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image476.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image477.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image478.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image479.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image480.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image481.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image482.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image483.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image484.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image485.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image486.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image65.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image487.png)

Figure 58 - Alice's clock slows down closer to a gravitational source as she is off the geodesic

Lest this business about time-dilation sound somehow “just math,” rest assured, as was the case in Special Relativity, it essential to GPS and much other technology that rely on clocks in gravitation fields. It is firmly baked into our engineering toolkit.

#### Gravitational Lensing

The most direct evidence that spacetime curvature is a thing unto itself, and not some “alternate way of describing a mass-proportional force-at-a-distance is that it affects light as well as matter. Light bends when passing through a gravitational field allow us to observe interstellar objects that otherwise would be eclipsed by objects in from them. The picture below illustrates this effect.

<figure>
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image488.jpeg" style="width:3.22917in;height:2.42188in" alt="Gravitational microlensing, illustration - Stock Image - F022/8898 - Science Photo Library" />
<figcaption><p>Figure 59 - Spacetime curvature allows light rays bend around objects</p></figcaption>
</figure>

#### Black Holes

Black holes are the result of there being a mass density sufficient to curve spacetime (radial distance vs time) more than 45 degrees with respect to base flat spacetime. When this happens, the light-like paths defining the boundary of light cones align with a specific radial distance that defines the event horizon of the black hole.

<figure>
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image489.jpeg" style="width:4.51389in;height:2.82913in" alt="Tipping the Light Cone: Black Holes | Asymptotia" />
<figcaption><p>Figure 60 - When light cones tilt by 45 degrees, no light can escape the event horizon, labelled here as 2M</p></figcaption>
</figure>

At this point any light emitted can, at best, skim the perimeter of the blackhole, the “event horizon.” Once beyond the event horizon, curvature causes the light-cones to tilt ever more, sealing the fate all bodies to fall to the center. In a sense, inside a black hole time and space switch roles. Whereas in flat spacetime, you can pass time without moving toward a different position, in a blackhole, you cannot pass time without moving toward the center, the “singularity,” – the time a clock ticks off proceeds in exact lockstep with your descent to the center. You can resist falling to the singularity by, say, firing rockets, but that only hastens your fate, as non-inertial motion decreases proper time, of arriving at the singularity, where we have no conception of measuring rods and clocks.

#### Gravitational Waves

Perhaps nothing illustrates the clear physical existence of the gravitational field more than gravitational waves. Fields, like stretched drumheads, pond surfaces or violin strings support ripples across their surface. Gravitational waves propagate exactly like waves on these surfaces do. That is evidence enough, but the incontrovertible signature of the field’s existence is that gravitational waves travel in regions with no massive-energetic sources. Let’s consider an analogy. You and I stand at opposite ends of a taut rope. When you shake your hand, my hand is thereby shaken. I conclude there is some invisible force linking your hand to mind, but you offer a different theory. You say that there is a rope between us that you are “driving” and it is the rope that shakes my hand. I say, how can we know the difference, and you suggest we devise some experiment that looks at a segment of the interval between us that neither of us are in. We build some enclosure around this section and, sure enough, hear the rope “humming.” Such is the evidence, in general, for the existence of fields.

Gravitational waves have, in fact, been detected. The concept is odd because the thing that is “vibrating” is not some “separate quantity” – like rope displacement – in spacetime, but spacetime itself, or, more formally, the distance metric on base, flat spacetime.

An essential – the essential – aspect of General Relativity and the other similar “driving substance / vibrating field,” so-called “gauge theories,” of other forces we will see is that the flow of the driver – matter-energy in the case of gravity – and the field – the metric in the case of gravity – live in a state of reciprocal, “coupled,” influence.

As an analogy, the material fields we see in life – ponds, drumheads, violin strings – are made of matter whose bonds explain the elasticity of the medium that supports waves. But our gravitational field is made of nothing. It is primary, fundamental. Where, then, does its elasticity come from? The answer to this does not quite address the question head-on. Instead, it says, “behaving like a material field with elasticity is the only way a hypothetical spacetime metric mechanism could behave.” Let’s see how this works. First, before we even have a field at all, we have the requirement of locality. That is, we can only affect our immediate neighbors, and this immediately suggests something that permeates spacetime, which is the essence of a field. Next, we know that we need to build an invariant so that we can extremize it. We know the invariant must include the field’s value – that is why we constructed the field. In the case of gravity, the value is the metric. Next, we know that the invariant includes the field’s derivative, for without that, there would be no notion of change. Now we need to “square” (contract using the Minkowski metric to find a norm) both the field value and derivative to have Lorentz invariant quantities. This leaves only the question, “why not use higher order derivatives or powers”? And the answer to that is 1) we don’t need to, we can build an invariant without them, and 2) there is always a regime in which first order approximations are valid. If extremizing a Lagrangian with only first order derivatives and lowest order powers did not provide the correct physical evolution, we could choose differently, but in practice, this appears to always work for the regimes we live in. We thus (accurately) speculate that a generic valid field Lagrangian at lowest order has the form

``` math
L = \frac{1}{2}(\partial_{\mu}\phi)(\partial^{\mu}\phi) - \frac{1}{2}m^{2}\phi^{2},
```

which is the standard Lagrangian for small oscillations of a field. The full gravitational field is tensorial and described by the a specific action, but in the regime of small ripples (gravitational waves) its behavior locally reduces to this same wave-like structure.

But this is the exact Lagrangian for a wave on a pond, drumhead, or violin. Is spacetime “elastic”? It would seem so. What is beneath it accounting for the tension? There isn’t an answer. As Wittgenstein said, “explanations come to an end somewhere.”

## Gauge Forces

We have seen that gravity is not a force in the sense of being “felt,” but that it nonetheless brings objects together by curving spacetime’s geodesics. On the other hand, a felt force, one that an accelerometer would register, entails moving off the spacetime geodesic. We can arrange this by firing a rocket or compressing a spring, what have you, but these are not fundamental forces. They are composed of fundamental forces, namely, of the electromagnetic force. Where do we “look” for fundamental forces beyond the curvature of spacetime? We look back to the elements already in hand – Poincaré symmetry, its representations, and the unitary operators that implement those symmetries.

Using these ingredients, we model a matter distribution by a complex wave function,

``` math
\psi(x),
```

a function over spacetime whose squared magnitude encodes measurable probabilities. We evolve this wave function using a unitary operator that represents a symmetry transformation. For example, a spacetime translation is implemented by

``` math
U(a) = e^{- i\text{ }a_{\mu}{\widehat{P}}^{\mu}},
```

where $`a^{\mu}`$is the translation parameter and $`{\widehat{P}}^{\mu}`$ is the generator of translations.

Because $`U(a)`$ enacts a symmetry, applying it does not change the physical state of the system. Its action amounts only to a change in the phase structure of the wave function:

``` math
\psi(x)\text{\:\,} \longrightarrow \text{\:\,}\psi'(x) = e^{- i\text{ }a_{\mu}{\widehat{P}}^{\mu}}\text{ }\psi(x)
```

And, as we have seen, when we the square the wave function to extract probabilities, the phase drops out, thus justifying the claim that it is a symmetry.

``` math
\mid \psi'(x) \mid^{2} = (e^{- i\text{ }a_{\mu}{\widehat{P}}^{\mu}}\psi(x))^{\text{ ⁣}*}(e^{- i\text{ }a_{\mu}{\widehat{P}}^{\mu}}\psi(x)) = e^{+ i\text{ }a_{\mu}{\widehat{P}}^{\mu}}\text{ }e^{- i\text{ }a_{\mu}{\widehat{P}}^{\mu}}\text{ } \mid \psi(x) \mid^{2} = \mid \psi(x) \mid^{2}.
```

The common way to view this geometry is that we have a copy of the phase angle space, that is U1 or “circle” space, at every point in spacetime. Since phase angle is symmetry, we must be able to advance the phase at every point by some amount without affecting the physics. This type of space is called a *fiber bundle*, which one can helpfully imagine as being similar to seaweed undulating on the seabed floor, where the seabed plays the role of the spacetime base space and each undulating strand of seaweed plays the role of a fiber (a “line,” not a “circle” in this visual analogy) and some slidable bead on each strand of seaweed is analogous to the phase at that point. The so-called “global phase symmetry” we’ve described is like moving each mark up or down its strand in unison.

### Local Symmetry

Let’s step back and think about how to interpret global symmetry. A useful analogy is currency in financial system. Currency “refers” to goods, but it is not a good itself. This role as of referring to a tangible thing automatically bestows global symmetry on currency. Rescaling matters not as long as whatever scale there is well-defined. The wave function phase is not a scale, it doesn’t expand and contract, but the idea is the same – any phase can equally well refer the same probability. Now, we can imagine a world with a single currency. We would be free to rescale the global currency, but it would be the same currency country to country. This, however, is not the world we live in. Instead, we live in a world in which every country is free to define their own currency, and our system of trade depends on an exchange rate that ensures we can measure equal value in different currencies, each with their own scale. We can make a similar claim about the wave function phase – each point in spacetime, we claim, has its own, independent, phase angle. If we do claim this, we must then have a rule for comparing phase from point to point If we do not, the Lagrangian the we build will not be invariant under Poincare symmetry transformation. In order to allow local phase symmetry and ensure the invariance of the Lagrangian, the rules that compare phase are, as we will see, constrained to a particular form. Spoiler alert – that form is exactly the general pattern from which Maxwell’s equations for electricity and magnetism are extracted.

Perhaps you object to this claim – why should we assert such a thing? We offer three answers, only the first of which we have much confidence in:

1.  If we *do* make this (kind of) assertion, all the known physical theories from the electromagnetic force to the weak and strong forces, and even, in the right formulation, gravitation, emerge.

2.  We see from financial currency, if not from other examples, that local symmetry is plausible.

3.  Unless the Lagrangian specifically depends on point-to-point absolute phase difference, there is nothing ruling out local phase symmetry.

In the Einstein field equation, we equated the metric field to the distribution and flow of matter. Similarly, we will see that the structure that tells us how to compare phase from point to point has a reciprocal relationship with the flow of “charge.” Also, as with the Einstein field equation, we will see that this structure-conferring field carries waves, namely electromagnetic waves, or light.

Specifically, if we allow the fiber value to “float” at every point, allowing this symmetry variation in the Lagrangian will manifest as a change to the Lagrangian’s value, that is, breaking its invariance. To “fix” this, at each point, we need a value that “cancels out” the arbitrary value-reference choice for each fiber, thereby providing a basis for parallel transport of the fiber value across spacetime. If a chosen local convention varies so that phase labels would differ between nearby points, the connection supplies an equal and opposite contribution to the corrected, or “covariant” derivative, ensuring that a physically constant phase is treated as constant. It may seem that this is sophistry. What is local phase symmetry if we posit another field that cancels out the gradient this symmetry suggests? The resolution is that local symmetry does render neighbor-to-neighbor gradients physically inconsequential, but the signature of the local symmetry lives not in the value of the connection field at any point (which is, by construction, also locally symmetric), but in curvature of the connection field that dictates what constitutes parallel transport of the phase.

This “connection field” is also called a “gauge field,” and theories built up in this way from local symmetries, or redundancies, are called “gauge theories.” The term “gauge” is not terribly instructive, but is, so we will use it. The basic idea, for what it’s worth, is that the measurement of phase depends on the choice of rod, or “gauge” to perform the measurement.

The curvature of the gauge field is defined as we always define curvature geometries, by how a thing being parallel transported changes around a loop. For example, if a vector is parallel transported around a loop on sphere, it gains a change in direction.\
\
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image490.png" style="width:3.66667in;height:3.09722in" alt="Parallel Transport | Galileo Unbound" />

*Figure 61 - Example of parallel transporting vector on a sphere*

If parallel transport around a loop in fiber bundle (that is, returning to the same spacetime point) results in a net phase change, then the connection field has curvature and the natural, the geodesic path through the fiber bundle follows this curvature. But following this path will generally not follow a spacetime geodesic (given by General Relativity) and thus manifests as a force, the strength of which is determined by how the *charged matter* *couples* to the gauge field.

These ideas are terribly abstract when first encountered. Fortunately, there is an everyday example that capture there essence – the flow of goods across different systems of currency.

### Finance as a Gauge Theory

Consider goods being traded between countries. The flow of goods is analogous to the flow of matter in physical space. People pay for goods in currency, but the value of a good in any given currency is arbitrary. An ounce of copper’s intrinsic value cares not if we inflate the dollar. We thus have the notion of global currency symmetry, or redundancy – any choice of currency scale will do for a system of trade. We can represent this situation mathematically with a fiber bundle. The base space is the 2-dimensional grid of countries, and the fiber is currency at each country-point.

Now, we not only have one global currency that we can rescale. We have different currencies on each fiber, each free to rescale on their own. Of course, if they do, we mush have an exchange rate table to tell us how to fairly exchange goods. The connection field, or gauge field, is the exchange rate between countries.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image491.png)

*Figure 62 - Fiber bundle for trading goods*

\[Pic above needs lots of help, just hard to draw with limited ink resolution\]

Consider a base space with just 3 countries, Italy, France, and Germany and consider two possible table of exchange rates:

|         | Italy              | France             | Germany            |
|---------|--------------------|--------------------|--------------------|
| Italy   | n/a                | 1 franc = 300 lira | 1 mark = 1000 lira |
| France  | 1 franc = 300 lira | n/a                | 1 franc = 0.3 mark |
| Germany | 1 mark = 1000 lira | 1 franc = 0.3 mark | n/a                |

*Figure 63 – “Flat” exchange rate space\*

<table style="width:100%;">
<colgroup>
<col style="width: 24%" />
<col style="width: 24%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<thead>
<tr>
<th></th>
<th>Italy</th>
<th>France</th>
<th>Germany</th>
</tr>
</thead>
<tbody>
<tr>
<td>Italy</td>
<td>n/a</td>
<td><table style="width:1%;">
<colgroup>
<col style="width: 1%" />
</colgroup>
<tbody>
</tbody>
</table>
<p>1 franc = 300 lira</p></td>
<td>1 mark = 1000 lira</td>
</tr>
<tr>
<td>France</td>
<td><table style="width:1%;">
<colgroup>
<col style="width: 1%" />
</colgroup>
<tbody>
</tbody>
</table>
<p>1 franc = 300 lira</p></td>
<td>n/a</td>
<td>1 franc = 0.35 mark</td>
</tr>
<tr>
<td>Germany</td>
<td>1 mark = 1000 lira</td>
<td>1 franc = 0.35 mark</td>
<td>n/a</td>
</tr>
</tbody>
</table>

*Figure 64 - Curved exchange rate space*

Now consider a copper trader, working in a system of exchange rates in the first table.\
\
Start with 300 lira

1.  Start with 300 lira

2.  Buy 1 oz copper

3.  Sell copper in France → 1 franc

4.  Convert francs to marks → 0.30 mark

5.  Convert marks to lira → 300 lira

End: 300 lira\
Profit: 0

But consider the second case:

1.  Start with 300 lira

2.  Buy 1 oz copper

3.  Sell copper in France → 1 franc

4.  Convert francs to marks:\
    1 franc → 0.35 mark

5.  Convert marks to lira:\
    0.35 mark → 350 lira

End: 350 lira\
Profit: +50 lira

Copper now flows in a loop, there is a copper *current* due to the curvature of the connection space. At each trade, the copper follows parallel transport (each trade was made using the established exchange rate, but due to the curvature of the connections, a “force” over “space” was created, compelling copper to flow. Moreover, the connection field – the exchange rate field – can support its own dynamics, as demonstrated by currency rescaling shocks.\
\
The example of finance offers is analogous to physical gauge theories and offers tactile appreciation. We can discuss how physics uses gauge theory.

### Gauge Theories in Physics

Everything we have discussed about dynamics proceeds from applying variational methods to extremize action. This defines parallel transport for physical systems and leads to the Euler-Lagrange equations of motion. To remind ourselves, the action that we extremize is the integral of the Lagrangian density over spacetime:\
\
``` math
{S\text{\:\,} = \text{\:\,}\mathcal{\int L}\text{ }d^{4}x
}
{And\ the\ Lagrangian\ density\ is\ composed\ of\ field\ terms\ that\ are\ invariant\ under\ symmetry\ transformations:}
```

``` math
\mathcal{L}\text{\:\,} = \text{\:\,}(\partial_{\mu}\phi)(\partial^{\mu}\phi)\text{\:\,} - \text{\:\,}m^{2}\phi^{2}\text{\:\,} + \text{\:\,}higher - order\ terms
```

That is, the Lagrangian density is composed of invariant combinations of fields and their spacetime derivatives.

Using these same elements and same variational approach, we can formalize the idea that forces arise from parallel transport through fiber bundles.

#### \
Global Symmetry and the Continuity Equation in Fields

Noether’s first theorem establishes a result we have already argued for on more intuitive grounds. We have said that if there is a symmetry, there is “no reason not” for its generator to be conserved. It states that any symmetry of the Lagrangian has an associated conserved current. That is, given a Lagrangian, it provides a procedure for picking out the conserved generator.

Consider some field whose action is invariant under U1 (or any one parameter) symmetry transformations on fibers. In this case, in 4-vector notation, the conserved current is then:

``` math
\partial_{\mu}j^{\mu} = 0
```

This is called the “continuity equation.” It is more intuitive if we split it into time and space coordinates:

``` math
\frac{\partial j^{0}}{\partial t} + \nabla \cdot \mathbf{j} = 0,
```

In words, this is saying the change in density inside a region equals the net flux through the boundary. This is a stronger and more satisfying statement of conservation than the abstract “conservation of momentum” statement we learn in high school physics. It is saying whatever the current represents – be it mass, charge, etc. – can neither be created nor destroyed at a point. It can only flow from one region to another.

From the continuity equation, one may define a global quantity by integrating the time component of the current over space,

``` math
Q = \int j^{0}\text{ }d^{3}x.
```

The continuity equation implies that $`Q`$is constant in time. This quantity is called the Noether *charge* (electrical charge being an example) associated with the symmetry.

We will not derive this result, but the path to it is nearly identical to the extremization method we used to derive that Euler-Lagrange equation for a straight line. In deriving the Euler–Lagrange equations, one considers an arbitrary variation of the fields, demands that the resulting variation of the action vanish, and then derives the equations of motion by necessity of the arbitrariness of the variation. Noether’s theorem follows this same route, but with a crucial restriction -- instead of allowing *arbitrary* variations of the fields, one considers only those variations generated by a symmetry of the action. It would be fair – and intuitive – to think of Noether conservation laws as narrower corollary of the Euler-Lagrange equations of motion. In any case, Euler-Lagrange and the continuity equation are facets of the invariance-under-transformation view that extremizing action presents.

This method for finding conserved quantities is enormously useful in doing physics as finding the full equations of motion may not always be possible, while the conserved currents can more easily be “read off” from the Lagrangian. In typical classical mechanics problems, a potential energy is given, and the potential may have certain symmetries but not others. For example, radial forces have orbital symmetry, thus angular momentum is conserved. However, as we will see, potentials are fundamentally stand-ins for interactions between free fields and their geometries, not primary objects in fundamental theories. On the other hand, we can apply Noether’s method to a free rigid body and find the associated conserved quantity is, as expected, momentum. And when we move from classical free rigid bodies to relativistic free fields, we identify each spacetime translation symmetry with a corresponding momentum current (whose time component is called energy).

#### Gauge Fields from Local Symmetry

To arrive at the continuity equation in Noether’s first theorem, we allowed variations under a global symmetry. We now ask, what if we allow variations under a local symmetry. For example, if we have a complex valued field, what happens if we claim that the phase can vary at each point without changing any physical observable, as is, in fact, asserted by the Born rule that all observables are given by the square of the wave function, which is independent of phase. We are going to use the example of the complex scalar field to work out how using the machinery of action variation explains gauge forces, but the example is only for illustrative purposes, it does not represent any real physical force. In fact, it is a close analog of actual forces. In the case of the electromagnetic force the major difference is that the field is spinor valued, and, in the cases of the strong and weak force, the difference is that fibers realize symmetries other than U(1). We will come back and revisit the example of electromagnetism when we have discussed quantum field theory.

Let

``` math
\phi(x)
```

be a complex-valued field defined over spacetime. As we mentioned earlier, the simplest Lorentz-invariant Lagrangian density we can build from this field is

``` math
\mathcal{L = (}\partial_{\mu}\phi^{*})(\partial^{\mu}\phi) - m^{2}\phi^{*}\phi
```

where $`\phi^{*}`$ is the complex conjugate of the field value. This Lagrangian is invariant under the global phase transformation

``` math
\phi(x)\text{\:\,} \longrightarrow \text{\:\,}e^{i\alpha}\text{ }\phi(x),
```

where $`\alpha`$is a constant. By Noether’s first theorem, this symmetry produces a conserved current,

``` math
j^{\mu} = i\text{ }\left( \phi^{*}\partial^{\mu}\phi-\phi\partial^{\mu}\phi^{*} \right),\ \ \ \ \ \ \ \ \ \ \partial_{\mu}j^{\mu} = 0.
```

Now, instead of a constant phase shift, consider a phase that varies with position:

``` math
\phi(x)\text{\:\,} \longrightarrow \text{\:\,}e^{i\alpha(x)}\text{ }\phi(x).
```

Under this transformation:

``` math
\partial_{\mu}\phi\text{\:\,} \longrightarrow \text{\:\,}e^{i\alpha(x)}\text{ }\left( \partial_{\mu}\phi + i(\partial_{\mu}\alpha)\phi \right),
```

and the Lagrangian is no longer invariant. The phase factor in the first term cancels out under the complex conjugation of the field derivative, but the extra terms proportional to $`\partial_{\mu}\alpha(x)`$ remain, and the action changes. Since we require that the action be invariant under symmetry transformation, it appears that local phase symmetry is a bust. But perhaps there is still some way to have our cake and eat it too. What this factor of to $`\partial_{\mu}\alpha(x)`$ is telling us is just what we should expect from the chain rule for derivatives – if we vary the phase angle in terms of the where the reference is, then that variation shows up in the derivative. This gives us a clue about how to restore invariance. We demand a field that cancels out the term arising from the symmetry variation itself:

Call this field $`A_{\mu}(x)`$, then define the *covariant derivative*:

``` math
D_{\mu}\text{\:\,} \equiv \text{\:\,}\partial_{\mu} + i{qA}_{\mu}.
```

Now, $`A_{\mu}`$ must be chosen so $`D_{\mu}\text{\:}`$varies under local phase symmetry in the same way as $`\phi(x)`$. That is:

``` math
{D_{\mu}\phi\text{\:\,} \longrightarrow \text{\:\,}(D_{\mu}\phi)' \equiv \text{\:\,}D_{\mu}'(\phi') = {D_{\mu}'\left( e^{i\alpha}\phi \right) = \ e}^{i\alpha(x)}D_{\mu}\phi
}
{Plugging\ away\ at\ the\ algebra\ gives:}
```

``` math
(\partial_{\mu} + iA_{\mu}')(e^{i\alpha}\phi) = e^{i\alpha}(\partial_{\mu} + iA_{\mu})\phi
```

And more rearrangement leads to:

``` math
A_{\mu}\text{\:\,} \longrightarrow \ A_{\mu}'\text{(x) = \:\,}A_{\mu}(x) - \partial_{\mu}\alpha(x)
```

``` math
```

What we have done is to say how $`A_{\mu}`$must transform under phase symmetry changes if it is to be used as to form the covariant derivative.

$`A_{\mu}`$ is the connection field we have discussed. Whether or not it is convincing that it has some physical substance, geometrically it is nothing elusive. It the same class of thing as, for example, the connection field we use to define parallel transport on a sphere. In that case, the connection tells you by how much to reorient a vector with respect to flat space in order to transport it along a geodesic on the sphere. Likewise, the connection field in our gauge theory for a complex field provides instructions for parallel transporting phase along the fiber bundle. If the connection field is curved, parallel transport around a loop results in a net change of phase angle. This phase gain is precisely the commutator of the transport generator, namely the covariant derivative:

``` math
\left\lbrack D_{\mu},D_{\nu} \right\rbrack\phi = iF_{\mu\nu}\text{ }\phi\ \ \ \ \ ,\ \ \ \ \ \ \ F_{\mu\nu} = \partial_{\mu}A_{\nu} - \partial_{\nu}A_{\mu}.
```

The quantity $`F_{\mu\nu}`$ measures the failure of parallel transport to close around an infinitesimal loop. When it vanishes, transport is path-independent and no force arises. When it does not, the natural trajectories in the full space project to accelerated motion in spacetime. That deviation is what we experience as force. While, again, our complex scalar field is not a real physical field, we nonetheless recognize $`F_{\mu\nu}`$ as the analog for *Faraday tensor*, which is the unifying structure behind Maxwell’s equations for electricity and magnetism!

We can now write an invariant Lagrangian with the covariant derivative:

``` math
\mathcal{L = (}D_{\mu}\phi)^{*}(D^{\mu}\phi) - m^{2}\phi^{*}\phi
```

In addition to these terms in the Lagrangian density, we also introduce a term for the gauge field’s own contribution. If we are to believe in the physical reality of local phase symmetry, we must also believe in the reality of the gauge field, and “reality” in physics means “contributes to the action.” Another argument for the “energetic reality” of the gauge field is that by construction it must exist in empty space independently of the matter field that gave rise to it. In any case, whether relying on the analogy to finance, arguing for it on logical grounds, or simply being willing to try it and see what happens, taking this leap from geometric measuring device to substance of the gauge field is borne out by the success of the theories it yields. Our term for the field Lagrangian density is:

``` math
{\mathcal{L}_{gauge} = - \frac{1}{4}F_{\mu\nu}F^{\mu\nu}
}
```
With the inclusion of this term, the full Lagrangian density becomes:

``` math
\mathcal{L = (}\partial_{\mu}\phi^{*})(\partial^{\mu}\phi) - m^{2}\text{ }\phi^{*}\phi\text{\:\,} + \text{\:\,}iqA^{\mu}(\phi^{*}\partial_{\mu}\phi - \phi\text{ }\partial_{\mu}\phi^{*})\text{\:\,} + \text{\:\,}q^{2}A_{\mu}A^{\mu}\text{ }\phi^{*}\phi\text{\:\,} - \text{\:\,}\frac{1}{4}F_{\mu\nu}F^{\mu\nu}.
```

And we now see the structure:\
``` math
\mathcal{L = (}SUBSTANCE\_ FIELD)\text{\:\,} + \text{\:\,}(COUPLED\_ INTERACTION\_ TERM)\text{\:\,} + \text{\:\,}(GAUGE\_ FIELD)
```

From here, we can go on to calculate specific forces, but we already see the structure in this schematic Lagrangian that is the basis of all fundamental forces. A “substance” field couples to a “gauge” field and, depending on the strength of the coupling, gives rise to the mutual interplay of the curvature of the gauge field causing non-inertial flows of substance, and the distribution of substance flows giving rise to curvature of the connection field.

Pseudo E&M Fields\
Now we can proceed to finding the force fields that are associated with this Lagrangian density. Caveat emptor! There is no complex scalar matter field in the nature we live in. We will use terms like E and B below to evoke the analogous electric and magnetic fields, but these are a “toy model,” not the real E&M fields which start with the spinor, not scalar, matter field.

Let’s start by writing out $`F_{\mu\nu}`$ in matrix form and try to fill in the elements:

``` math
F_{\mu\nu} = \begin{pmatrix}
F_{00} & F_{01} & F_{02} & F_{03} \\
F_{10} & F_{11} & F_{12} & F_{13} \\
F_{20} & F_{21} & F_{22} & F_{23} \\
F_{30} & F_{31} & F_{32} & F_{33}
\end{pmatrix}
```

By the anti-symmetric construction of the $`F_{\mu\nu}`$, the diagonal terms all vanish:

``` math
F_{00} = - F_{00} \Rightarrow F_{00} = 0
```

Also, by the anti-symmetry, the off-diagonal terms are related by:

$`F_{01} = - F_{10}`$ etc.

Thus, there are six independent slots.

Let’s label the three components that mix time and each spatial dimension, evocatively, as follows:

``` math
E_{x} \equiv F_{01},E_{y} \equiv F_{02},E_{z} \equiv F_{03}.
```

Likewise, let’s label the components that mix spatial dimensions as follows:

``` math
F_{23} \equiv B_{x},F_{31} \equiv B_{y},F_{12} \equiv B_{z}.
```
We now have:

``` math
F_{\mu\nu} = \begin{pmatrix}
0 & E_{x} & E_{y} & E_{z} \\
 - E_{x} & 0 & B_{z} & - B_{y} \\
 - E_{y} & - B_{z} & 0 & B_{x} \\
 - E_{z} & B_{y} & - B_{x} & 0
\end{pmatrix}
```

What we’re calling mixing “time and space” vs “space and space” has the following interpretation:

- In the worldline picture, $`F_{0i}`$ mixes time with space meaning it acts as a boost. Thus the E, or “electric field,” components act as a typical force – they cause a change in velocity.

- $`F_{ij}`$mixes spatial dimensions, so it only acts to change the direction of motion, not the magnitude of velocity.

If you have taken an E&M course, you have seen that the electric field looks like lines radiating radially from a charge source, while the magnetic field looks like a curl around a moving charge.

<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image492.jpeg" style="width:2.94051in;height:1.65068in" alt="Divergence and Curl of Electric Field" /> <img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image493.jpeg" style="width:2.98309in;height:1.65068in" alt="equations of electromagnetism ..." />

Figure 65 - Geometric Structure of Electric and Magentic Fields

Let’s now show that the field equations derived from our toy Lagrangian reproduce these same geometric features.

Recall that the time component of the current,

``` math
j^{0} = \rho,
```

is simply the charge density. Taking the $`\nu = 0`$component of the gauge field equation

``` math
\partial_{\mu}F^{\mu\nu} = j^{\nu},
```

and using our identification $`E_{i} = F_{0i}`$, we obtain

``` math
\partial_{1}E_{1} + \partial_{2}E_{2} + \partial_{3}E_{3} = \rho,
```

or, in vector notation,

``` math
\nabla \cdot \mathbf{E} = \rho.
```

This is the statement that electric field lines diverge from regions of nonzero charge density, exactly as suggested by the radial field pattern associated with static charges.

We now turn to the spatial components, which encode the magnetic field. The purely spatial part of the field equation,

``` math
\partial_{\mu}F^{\mu i} = j^{i},
```

involves the antisymmetric tensor $`F_{ij}`$, which we have identified with the components of $`\mathbf{B}`$. Writing this out explicitly,

``` math
\partial_{0}F^{0i} + \partial_{j}F^{ji} = j^{i}.
```

The first term involves time variation of the electric field, while the second term contains only spatial derivatives of the magnetic components. In the steady-current case, where fields are time-independent, the electric term drops out, leaving

``` math
\partial_{j}F^{ji} = j^{i}.
```

Because $`F_{ij}`$is antisymmetric, this combination of derivatives is precisely the curl. In vector notation, this becomes

``` math
\nabla \times \mathbf{B} = \mathbf{j}.
```

This equation expresses the geometric fact that magnetic fields do not begin or end on sources, but instead circulate around regions where charge is flowing. The antisymmetry of $`F_{ij}`$enforces this structure: spatial curvature generated by the gauge field can only appear as rotation, not divergence.

Taken together, these results show that our toy model reproduces the essential geometric distinction between electric and magnetic fields. Electric fields are associated with divergence and act to change the magnitude of velocity, while magnetic fields are associated with curl and act only to redirect motion. Although the underlying matter field here is scalar rather than spinorial, the geometric content of the gauge curvature already contains the familiar electric–magnetic split.

##### Dynamics and Force 

We can now ask what change takes place in a gauge theory. In fields, flow geometry replaces forces. We have two fields to keep track of, the matter field, which carries conserved quantities and whose evolution encodes the flow of substance through spacetime. And the gauge field, whose curvature defines how those flows are redirected. Neither field is auxiliary to the other, each contributes independently to the action, and each possesses its own degrees of freedom.

One could in principle vary everything at once. But doing so provides little insight. Recognizing that the two fields play different physical roles, we reveal those roles by varying the action with respect to each field separately.

First, consider variations of the matter field $`\phi`$, with the gauge field $`A_{\mu}`$held fixed. This yields the Euler–Lagrange equation for the matter sector of the theory:

``` math
(D_{\mu}D^{\mu} + m^{2})\phi = (\partial_{\mu} + iqA_{\mu})^{2}\phi + m^{2}\phi = 0.
```

In geometric language, this equation governs how the matter field propagates when parallel transport is dictated by a specified connection. (The mass term sets the intrinsic scale associated with the particle species supported by the field, a point we return to in the next chapter.) This equation plays the role of a force law in the particle picture, but in the field picture it describes how extended distributions evolve and deform in the presence of curvature.

Independently, the same matter Lagrangian is invariant under global phase rotations of the field. By Noether’s theorem, this symmetry implies the existence of a conserved current. When the matter field satisfies the equation above, the associated current is

``` math
{j^{\mu} = iq(\phi^{*}D^{\mu}\phi - (D^{\mu}\phi)^{*}\phi)
}
```
satisfying the continuity equation:

``` math
\partial_{\mu}j^{\mu} = 0.
```

which represents the flow of a conserved quantity through spacetime.

Next, consider variations of the gauge field $`A_{\mu}`$, with the matter field held fixed. This variation yields the field equation governing the gauge field itself:

``` math
\partial_{\mu}F^{\mu\nu} = j^{\nu}\ \ \ ,\ \ \ \ \ \ F_{\mu\nu} = \partial_{\mu}A_{\nu} - \partial_{\nu}A_{\mu}.
```

This is telling us the gauge field curvature given a specific current sourcing the field.

Putting these coupled field equations together, we see their reciprocal relationship.\
\
``` math
\partial_{\mu}F^{\mu\nu} = j^{\nu}\ 
```

The configuration of the “matter field,” $`\phi`$, which includes coupling terms to the gauge field, tells us what the charge current is. The charge current then determines the gauge field curvature – which feeds back into the current.\
\
Now we can go one step farther and ask, how does 4-momentum distribution of the matter field evolve, that is, what is the field-native version of the “electromagnetic force on particle” one learns in E&M 101. To answer this, we consider the response of the action to spacetime translations. By Noether’s theorem, translational symmetry implies a conserved stress–energy tensor, satisfying:

``` math
\partial_{\nu}T^{\mu\nu} = 0
```

For the coupled matter–gauge system, the total stress–energy tensor can be written as a sum of matter and gauge contributions, leading to:*\*

``` math
\partial_{\nu}T_{\text{matter}}^{\mu\nu} = F^{\mu\nu}j_{\nu},
```

*\*
``` math
\partial_{\nu}T_{\text{gauge}}^{\mu\nu} = - \text{ }F^{\mu\nu}j_{\nu}.
```

or:

``` math
\partial_{\nu}(T_{\text{matter}}^{\mu\nu} + T_{\text{gauge}}^{\mu\nu}) = 0
```

We read this as saying that the force density — the rate at which momentum is transferred — is given by the gauge field curvature contracted with the current.


# Quantum Field Theory

Relativity flouts our intuition – measuring sticks themselves change with relative motions – but leaves our categories intact. Quantum mechanics demands a new categories altogether – we can no longer reason about a world filled with objects at definite locations but must instead probe nature to find statistical patterns. These theories constitute our modern insights into nature’s fundamental structure, but do not fit together to form a coherent and complete story. “Quantum field theory” is an attempt to address this. In this section, we will not encounter any new intuition-smashing result. Instead, we will recount the – often somewhat messy – synthesis that comprises our current fundamental model of all but gravity.

In presenting quantum field theory, we will first look at the gaps and inconsistencies of early quantum mechanics to understand why we need QFT. Next, we will discuss the major building blocks of the ontology, or fundamental constituents of reality, the theory asserts. We will then develop a simple working physical field model and using that make the decisive of step marrying the ideas of a classical field and quantum operators. At this point we will be able to say what it means to be a particle. We will complete this development of the core model by formally expressing the field theory in the algebraic structure of quantum canonical commutators. At this point we can ask ourselves what we are the building-block calculation we can make with such a theory. To approach these calculations, we will switch our approach from thinking about local differential equations to thinking about global action variation. This will lead to perturbative solutions and Feynman diagrams that give definition to our conception of discreet interactions. We will then move from our simple example field to actual matter and gauge fields, focusing particularly on the electron and photon fields, known collectively as quantum electrodynamics, or QED. Finally, as a pay off for the long journey to present physics at its most fundamental level, we will show that we can use QED to derive the familiar Coulomb electromagnetic forces.

## The Limits of Early Quantum Mechanics 

In its early development, the originators of quantum mechanics were too busy inventing a brilliant new formalism to express wildly counterintuitive evidence to, at the same time, offer a fully complete and coherent physical theory.

### Wherefore Particles?
The first conceptual gap in early quantum mechanics is that it offers no answer to the natural question: what is a particle? If one is happy with the operational definition that a particle is a sort of rigid object, this isn’t a problem, but this definition quickly becomes untenable in quantum theory. How can a rigid body have an uncertain location? What accounts for different particle types? How is a rigid body an irreducible representation of symmetry? When one learns about the particle nature of light demonstrated by the photoelectric effect, one may be tempted to think that a particle, in early quantum mechanics, is a “quantum,” a little parcel of energy. This is, in fact, what QFT will tell us, but early quantum mechanics does not say this. It explained how a particle confined to a location has quantized energy levels due to the need to fit its wave function into the potential, like harmonics fit on a guitar string. In fact, using early quantum theory, calculating these energy levels is an introductory undergraduate exercise. But there is no similar way to calculate that free energy must come in discrete quanta. From de Broglie’s equations, we do know the energy of a particle is related to frequency by $`E = h\nu`$, but this does not answer why additional energy must be added as discrete particles. QFT, through so-called “second quantization,” does take exactly this step, defining particles as quanta of excitation of a field in spacetime, where the discrete spectrum is still picked out by a boundary-condition-type requirement: the total probability across all field configurations must add up to some finite constant, which means that the probability assigned to arbitrarily large field amplitudes — and thus arbitrarily large energies — must die away. Second quanization uplevels the discreet spectrum associated with boundary conditions from the wave function to the wave functional of the field configuration. 

If particles are field excitations, what then are waves in the classical E&M field sense? The answer is that they are quantum fields in the case where many particles occupy the same mode. This is true for light but not for fermionic matter fields due to the Pauli exclusion principle, which prevents multiple fermions from occupying the same state. Now one might fairly ask, if the origin of particles is field excitations, what is the origin of the field? QFT offers no answer for this other than that it is the only object we know of that can meet the demands of spacetime symmetry and unitarity of state.


The second conceptual gap in early quantum mechanics is that it is not constructed on spacetime.


### Where is Spacetime
Early quantum mechanics is lacking a notion of local spacetime. If quantum mechanics is a theory only of probaility distributions over position, removing the the theoretic elements of bodies with trajectories, it is unmoored from spacetime. But Relativity demands that influence be local. Were this not the case, spatially separate locations on the same equal-time slice could influence one another, that is, their influence could act outside their light cones. But the wave function is not, in the classical sense, a field spread through spacetime that passes influence from neighbor to neighbor. It is an amplitude over position space or other dynamical variables, in the one-particle case over position space or some other dynamical variable, and in the many-particle case over configuration space. As such, it does not move through space. It is simply given on the whole slice at once, or, equivalently, moves at infinite speed. While this structure appears to present a causal contradiction, knowing what a slippery thing the wave function is, we will specify experiments that pin down what sort of spacelike influence this quantum formalism implies. 

We can see this relativistically impermissible structure directly in the Schrödinger equation,

$$
i\hbar \frac{\partial \psi}{\partial t}
=
\left(
-\frac{\hbar^2}{2m}\nabla^2 + V
\right)\psi.
$$

It is first order in time and second order in space, but in spacetime space and time stand, modulo the metric sign, on equal footing. That mismatch is already a strong clue that something is wrong. Equations of this kind belong to the broad family of diffusion equations, such as those describing heat flow, in which an amplitude spreads with exponential falloff but becomes immediately nonzero everywhere. In a relativistic setting that is impermissible, since influence should remain confined to the light cone.

From the Schrödinger equation’s solutions, we can find the dispersion relation,

$$
\omega = \frac{\hbar k^2}{2m},
$$

from which we find the group velocity,

$$
v_g = \frac{\partial \omega}{\partial k} = \frac{\hbar k}{m}.
$$

The speed of light appears nowhere in this equation, and thus the group velocity is unbound. In early quantum mechanics, barring pathological exceptions, group velocity is particle velocity, so the theory predicts that particle velocity can exceed lightspeed in an experimentally observable way. This is exactly what one should expect from a theory built for Galilean rather than Minkowskian spacetime.

We can devise an experiment to test this. Prepare a narrow free-particle wave packet with sufficiently large central wavenumber, let it propagate across a known baseline, and compare the arrival time of the packet peak to the light-travel time across the same distance. Since the group velocity in the theory is unbounded, the theory permits choosing the packet so that its peak arrives sooner than any light signal could.

One can see the same problem by starting from a localized state. Suppose that on some equal-time slice the particle is sharply confined to a small spatial region. Under Schrödinger evolution, that localization does not spread by advancing outward through neighboring points at some finite characteristic speed. It evolves according to

$$
\psi(x,t) = \int_{-\infty}^{\infty} \phi(k)\, e^{i(kx-\omega t)}\, dk,
$$

with

$$
\omega = \frac{\hbar k^2}{2m}.
$$

Since every Fourier mode is immediately present in the evolved state, the wave function acquires nonzero support arbitrarily far away after any nonzero time, however short. The tails may be tiny, but they are there at once. In a relativistic theory that matters. If a particle is localized here now, there must be regions elsewhere now that remain exactly outside causal reach. 

Here too the experiment is straightforward. Localize the particle near one detector on an equal-time slice, place a second detector far enough away that for a chosen short time window it is spacelike separated from the first, and then allow the state to evolve for that short time. Schrödinger evolution immediately assigns the distant detector a nonzero amplitude where relativity demands it be exactly zero.

### Making Particles

Early quantum mechanics fixes the particle count at the start. For $N$ particles, the state is a wave function on an $N$-particle configuration space,

$$
\psi(x_1,\dots,x_N,t).
$$

The number of particles is built into the space the state lives on. Time evolution can move amplitude around inside that space, but it cannot leave it. An $N$-particle Schrödinger theory can reshuffle the state of $N$ particles. It cannot turn $N$ into $N+1$ or $N-1$.

But particle creation in nature is commonplace. An excited atom emits a photon, and an energetic collision produces new particles. Matter and radiation exchange quanta. One may model different particle compositions with different Hilbert spaces, but that is exactly the point. The theory does not contain one unified state space in which particle composition may change.

QFT will fix this by changing what a particle is. In second quantization, a particle is not a primitive object that happens to carry energy. It is one step in the discrete excitation spectrum of a field mode. Once a mode is quantized, its occupation number, how many particles are in a given momentum mode, comes in levels $n=0,1,2,\dots$, and there are operators that move up and down that ladder,

$$
\hat a^\dagger |n\rangle \propto |n+1\rangle,
\qquad
\hat a |n\rangle \propto |n-1\rangle.
$$

These ladder operators imply an extension of state space to the direct sum of all fixed-particle-number spaces, called Fock space.

### Where Potentials Come From

Classical physics says "give me a potential energy function, and I will tell you a body's trajectory." What it does not say is the origin of that potential. It may label it, e.g., gravitation or electrical, but it takes the potential as a given, and proceeds from there. 

We see this in the form of a typical Hamiltonian, 

$$
H = \frac{p^2}{2m} + V(x),
$$

Early quantum mechanics likewise takes the potential as a given, 

$$
\hat H = \frac{\hat p^2}{2m} + V(\hat x),
$$

and then solves for the state in the prescribed environment. The hydrogen atom illustrates this point. The electron is treated quantum mechanically, but the Coulomb potential is simply posited. Likewise, a particle in a box is given walls, and a harmonic oscillator is given a restoring force. 

This approach is unassailably effective, but we a priori prefer a theory that explains what had been given in terms of a smaller number of theoretic elements. 

Classical electromagnetism takes a step toward giving an origin story for potentials. Rather than simply positing a potential function over space, it gives the field potential an energetic, dynamic body that evolves in accordance with Relativity. What this does not do, however, is provide a mechanism by which potential acts on matter. 

At the same time, as we have seen, gauge fields can provide such a mechanism, through the curvature of the connection field. However, before QFT, the role of the electromagnetic field as a connection for a matter field was not worked out. We will see that in QED (QFT for electromagnetism), there are fields associated with matter particles and a gauge field associated with photons whose curvature is responsible for the electromagnetic force. In the formalism, it will appear as an interaction term in the Lagrangian of the full system. Schematically, one writes

$$
\mathcal{L}_{\mathrm{QED}}
=
\mathcal{L}_{\mathrm{electron}}
+ \mathcal{L}_{\mathrm{photon}}
+ \mathcal{L}_{\mathrm{interaction}}.
$$

The first term is the electron-field dynamics, the second the photon-field dynamics, and the third their coupling. At that point the potential is no longer primitive. It survives only as an effective description of a deeper process in which fields interact locally.

## The Spaces of QFT
We are going to construct specific quantum fields, formalize their interactions, and make calculations with them. However, as QFT adds a layer of abstraction on top of the already extraordinarily abstract ideas of quantum mechanics and Relativity, when working through the details, one can feel they have lost sight of the concepts underlying the calculations. Therefore, let's start by discussing the theoretic elements of QFT, and let's do so by anchoring these in the language of spaces, for every element in a physical theory is reflected in the spaces it invokes, the structure of those spaces and the objects that inhabit them. 

We are biased to favor spacetime because it is the space we directly perceive, but nature is not required to privilege our perception. In physics, how influence transmits locally, how a complete state is specified, how symmetries constrain possibility, and how identity is preserved in a probabilistic world are organized in the interplay of multiple spaces. To best appreciate the elements of  QFT, let's begin by reviewing the spaces of classical and early quantum mechanics, and then turn to the changes made by QFT.

### Spaces in Hamiltonian Mechanics

A classical theory must distinguish a **state at an instant** from a **history through time**. A history is the full trajectory. A state is the information on one time slice from which that trajectory can be generated. In Hamiltonian mechanics that state is organized in **phase space**. For finitely many degrees of freedom one writes

``` math
z = (q^{i},p_{i}),
```

and for a classical field one writes, on a time slice,

``` math
z = (\phi(x),\pi(x)).
```

The variables $q^{i}$, or $\phi(x)$ in the field case, specify the configuration. The variables $p_{i}$, or $\pi(x)$, specify the conjugate momentum. We stress “on a time slice” because spacetime contains entire histories, while dynamics asks a different question: what present state is enough to determine the future.

One could try to organize the state using position and velocity. For simple systems that often works. But momentum is not just velocity renamed. It is defined from the Lagrangian by

``` math
p_{i} = \frac{\partial L}{\partial{\dot{q}}^{i}},\pi(x) = \frac{\partial L}{\partial\dot{\phi}(x)}.
```

In the simplest cases momentum is proportional to velocity. In general it is not. The distinction matters in generalized coordinates, in relativistic systems, in gauge theories, and in field theory. More importantly, momentum lets us rewrite the theory in a form that carries much more structure than a bare position-velocity description. The state is no longer just “where things are” and “how fast they are changing.” It is organized into conjugate pairs, whose structure we will unpack. The upper index on $`q^{i}`$and the lower index on $`p_{i}`$are distinguishing two different kinds of object. An infinitesimal displacement $`dq^{i}`$is a position-type change. The momentum $`p_{i}`$is the corresponding dual object, written with a lower index because its role is to combine with such a displacement to produce the scalar quantity

``` math
p_{i}\text{ }dq^{i}.
```

This pairing is the first sign that phase space is not an arbitrary list of variables. Once the rate data are written in this momentum form, position and momentum fit together in a built-in geometric structure.

That built-in structure is the symplectic form,

``` math
\omega = dq^{i} \land dp_{i}.
```

Here $`dq^{i} \land dp_{i}`$represents the infinitesimal oriented area in each position-momentum plane. So the symplectic form is the phase-space area structure. It tells us that the basic geometry of phase space is not a geometry of lengths and angles, but a geometry of paired position-momentum areas.

This matters because that area structure turns functions into flows. A function on phase space, such as the Hamiltonian, tells us how its value changes under small moves away from a point. The symplectic structure converts that change-data into a vector field, meaning an actual direction of motion through phase space. In this sense, the symplectic form is the rule that turns gradients into flows.

The Poisson bracket is the algebraic expression of that rule. For two functions $`F`$and $`G`$on phase space,

``` math
\{ F,G\} = \frac{\partial F}{\partial q^{i}}\frac{\partial G}{\partial p_{i}} - \frac{\partial F}{\partial p_{i}}\frac{\partial G}{\partial q^{i}}.
```

This bracket tells us how the flow generated by one function acts on another. Classical observables are then ordinary functions on phase space,

``` math
A = A(q,p)\text{or}A = A\lbrack\phi,\pi\rbrack.
```

When the generating function is the Hamiltonian $`H`$, the resulting flow is physical time evolution. Hamilton’s equations are

``` math
{\dot{q}}^{i} = \{ q^{i},H\},{\dot{p}}_{i} = \{ p_{i},H\}.
```

So the symplectic form, the Poisson bracket, and Hamilton’s equations are three parts of one structure. The symplectic form gives phase space its position-momentum area geometry. The Poisson bracket is the corresponding algebra on functions. Hamilton’s equations are the flow generated by the energy function within that geometry.

Because the flow is generated in this way, it preserves the symplectic structure itself. In the simplest picture, a region of phase space may be stretched and sheared as the system evolves, but its basic position-momentum area is not destroyed. In higher dimensions the corresponding phase-space volume is preserved as well. This property is known as Liouville’s theorem, which states that a statistical ensemble of initial conditions, however it evolves, occupies the same phase space volume.

Phase space therefore does more than store enough information to start the system evolving. It organizes the classical state in a form that makes time evolution a vector flow, gives a natural bracket algebra on observables, preserves phase-space volume, and supplies exactly the structural features that quantum mechanics will keep in translated form. In quantum theory, the Poisson bracket becomes the commutator, and the structure-preserving role played here by symplectic flow reappears in the preservation laws of unitary evolution. Some people say Hamiltonian Mechanics is the “river of time” formulation of mechanics. Indeed, by picking a conjugate pairing of position and momentum, we can see time evolution as a vector flow, as though in a fluid, and Liouville’s theorem is that statement that this fluid in incompressible.

Spacetime enters classical theory as the space in which events occur and in which local dynamical (changing over time) quantities are assigned. In classical particle mechanics a trajectory is a worldline in spacetime. In classical field theory the basic variables are already local functions on spacetime,

``` math
\phi(x)\ (scalar),\ \ \ \ \ A_{\mu}(x)\ (vector),\ \ \ \ \psi(x)\ (spinor),
```

and causality is built into their equations of motion. A relativistic classical field theory inherits adherence to the structure of Relativity “for free” because its state variables already inhabit spacetime. This seems obvious, but we will see how quantum mechanics breaks this relationship.

Symmetry groups that constrain dynamics like the Poincare group reside in their own space, whose geometric structure constrains the theory. In Hamiltonian mechanics each continuous symmetry has a generator, a function on phase space, and the Poisson brackets among the generators reproduce the Lie algebra of the symmetry group:

``` math
\{ G_{a},G_{b}\} = f_{ab}{}^{c}\text{ }G_{c}.
```

This is the local algebraic shadow of the group geometry. For example, for angular momentum,

``` math
\{ J_{i},J_{j}\} = \epsilon_{ijk}J_{k}.
```

For spacetime symmetry one gets the classical Poincaré algebra. The meaning is direct: the way infinitesimal transformations fail to commute is fixed by the structure of the symmetry group itself.

Symmetries therefore already act physically in classical mechanics. A generator $`G`$ produces an infinitesimal canonical transformation by

``` math
\delta F = \{ F,\epsilon G\}.
```

The group geometry is reflected in the Poisson algebra, and the Poisson algebra acts on the phase-space observables.

The minimal classical picture is therefore this. Spacetime carries locality and causal order. Phase space carries complete instantaneous state data and symplectic structure. Symmetry structure supplies invariants and generator algebra.

### Quantum mechanics

Quantum mechanics keeps the classical need for spacetime, canonical structure, and symmetry, but it adds something genuinely new. The classical state was a point in phase space. The quantum state is not. It is a vector, or more precisely a ray, in a complex Hilbert space $`H`$.

This new space is required to carry the structure demanded by superposition, interference, and probabilistic prediction. A point in phase space singles out one actual configuration and momentum, but quantum state assigns amplitudes to many alternatives at once *for the same state*. We must, therefore, have a space that can preserve the structure of such states as time evolves.

The observables are now self-adjoint, or real-eigenvalued, operators on $`H`$. In ordinary one-particle quantum mechanics one may represent the state as a wavefunction

``` math
\psi(x) = \langle x \mid \Psi\rangle.
```

Now, we could look at this and think that we’ve represented the state in spacetime, but we have not, for this is a representation over space only, and we could just as easily have represented the state in the basis of any other observable. Time evolution acts on the state as a whole in Hilbert space, and nothing in this representation ties that evolution to position in a way that builds in relativistic locality. Without that, there is no Minkowski metric, no light cones, and no causal structure of the sort that defines the spacetime in which our emitters and detectors live. But what if we could somehow arrange the time evolution of the state so that emission and detection events do respect the proper causal structure. That is what we will do in QFT.

While Hilbert space does not carry the needed structure of spacetime, it does take over structural elements of phase space’s job. Hilbert space looks very different from phase space. We know it encodes superposition rather than definite observable values, but it also is represented in the eigenbasis of only one chosen observable at a time. How can a space that is represented in a basis of “either position or momentum” replace a space whose coordinates were “position and momentum”? The reason it can do so is that, unlike particles, the wave object encodes both position and wavelength information. Once we associate wavelength with momentum, the wave-like state encodes position and momentum.

We have seen that Hilbert space contributes to the structure needed for quantum evolution. A complex inner product gives a norm, so states can be normalized and total probability can remain one. It also gives angles, so distinct states can remain distinguishable under unitary evolution. But the same inner product carries more than length and angle. Through the magic of complex numbers, Hilbert space’s real and imaginary parts bear different loads. The real part supplies the metric-like structure just mentioned. The imaginary part supplies an antisymmetric, area-like structure that is the quantum remnant of the classical symplectic form, $`dq^{i} \land dp_{i}`$.

If $`\langle\psi,\phi\rangle`$is the complex inner product, then its real and imaginary parts define

``` math
g(\psi,\phi) = 2\text{ }Re\text{ }\left\langle \psi,\phi \right\rangle,\ \ \ \ \ \ \ \ \ \ \ \ \ \omega(\psi,\phi) = 2\text{ }Im\text{ }\langle\psi,\phi\rangle.
```

Here $`g`$ is symmetric and metric-like. The second quantity, $`\omega`$, is antisymmetric. We can see this with a simple example. Writing $`z\  = x + iy,\ \ \ \ w = u + iv`$:

``` math
{\langle z,w\rangle = xu + yv + i(xv - yu).
}
```
That antisymmetric part is exactly what one needs for a symplectic form. (This is just the signed area of the parallelogram spanned by $`\left( x,y \right)`$and $`\left( u,v \right)`$:

``` math
{\text{Area} = \  \mid xv - yu \mid .
}
```
With this symplectic structure retained in translated form, Hilbert space preserves the part of classical mechanics concerned with reversible flow and conjugate pairings. In classical phase space, position and momentum were paired by the symplectic form, and that pairing gave rise to Hamiltonian flow through the Poisson bracket:

``` math
\{ F,G\} = \frac{\partial F}{\partial q^{i}}\frac{\partial G}{\partial p_{i}} - \frac{\partial F}{\partial p_{i}}\frac{\partial G}{\partial q^{i}}.
```

Quantum mechanics preserves that structure in operator form, replacing the Poisson bracket with the commutator,

``` math
\{ F,G\}\text{\:\,} \longrightarrow \text{\:\,}\frac{1}{i\hslash}\lbrack\widehat{F},\widehat{G}\rbrack,
```

Which for canonical position and momentum becomes:

``` math
\lbrack{\widehat{q}}^{\text{ }i},{\widehat{p}}_{j}\rbrack = i\hslash\text{ }\delta^{i}{}_{j}.
```

Symmetry works in quantum mechanics much as it did in Hamiltonian mechanics, except that Poisson brackets are replaced by commutators. If the symmetry group is the Poincaré group, one may represent it on Hilbert space, so ordinary quantum mechanics can describe how states transform between inertial observers and can correctly encode quantities such as energy, momentum, and spin. But this is not yet relativistic causality. Causality is not just the statement that whole states transform correctly. It is the statement that operations associated with spacelike separated regions do not interfere in a way that would permit superluminal influence. A representation of the Poincaré group on states does not by itself provide spacetime-local observables or require the appropriate commutation relations between them. That is the additional structure QFT must supply.

### Quantum field theory

Quantum field theory adjusts the roles of spacetime and Hilbert space so that quantum observables carry local spacetime structure, and so that interactions can create and destroy particles.

In quantum mechanics there are two objects that work together to calculate measurements, the state and the operators. If we want to bring spacetime into quantum mechanics, it is natural to ask whether one or the other should be situated in spacetime. Since operators are observables, they are the natural choice. The state, by contrast, is better understood as a global object, whose job is to encode the amplitudes and correlations from which measurement outcomes are computed. If we want the operators to depend on spacetime, we must further specify what sort of local spacetime structure they inhabit: discrete points, as in a particle configuration, or a field, as in electromagnetism and gravity. In fact, only fields can mediate influence relativistically. If influence could act directly across a spacelike gap, then because spacelike separated events have no observer-independent time order, one observer’s cause could be another observer’s effect, opening the door to causal paradox. Influence cannot simply jump the gap. But once it does not jump the gap, whatever later makes a difference elsewhere must be instantiated in the intervening region while it is on its way. The moment one says that information propagates, one has already admitted local degrees of freedom that carry it from place to place. In the continuum, that distributed local state is by definition a field.

We can now state this in notation. The basic local objects are operator-valued fields:

``` math
\widehat{\phi}(x)\text{~[scalar]},\widehat{\ \psi}(x)\text{~[spinor]},{\ \ \ \widehat{A}}_{\mu}(x)\text{~[vector]}.
```

More carefully, because exact point values are singular, one should work with smeared operators,

``` math
\widehat{\phi}(f) = \int d^{4}x\text{ }f(x)\widehat{\phi}(x),
```

and similarly for the other fields.

Once the basic observables are placed in spacetime, relativistic causality can be stated directly:

``` math
\left\lbrack \widehat{O}(x),\widehat{O}(y) \right\rbrack = 0\ \ \ \text{for~spacelike~separated~}x,y.
```

This is how relativistic causality is expressed in commutator algebra. It says that the order of two spacelike separated operations has no physical effect. A representation of the Poincaré group on state space alone was not enough, because this new condition presupposes local observables attached to spacetime regions.

A state in Hilbert space is still an amplitude assignment over possible alternatives, but now those alternatives are entire field configurations written in the eigenbasis of field operators.If $`\mid \phi\rangle`$ denotes a field-configuration eigenstate at fixed time $`t`$, then

``` math
\widehat{\phi}(x,t) \mid \phi\rangle = \phi(x) \mid \phi\rangle,
```

and the state may be represented as a wave functional,

``` math
\Psi_{t}\lbrack\phi\rbrack = \langle\phi \mid \Psi(t)\rangle
```

thus shifting the notion of locality to the field itself rather than trying to exist in the position representation of the state.

We can see how this provides the needed spacetime constraint by looking at an example. Consider two localized interventions, one in region $`A`$ near “Alice” and one in region $`B`$ near “Bob,” with $`A`$ and $`B`$ spacelike separated. Alice changes something in her lab. Bob asks whether his detector statistics change immediately.

In ordinary one-particle quantum mechanics, Alice’s intervention is represented by modifying the Hamiltonian near $`A`$, but the state is global and the theory has no condition forbidding that change from having an immediate effect at spacelike separated $`B`$. It can represent position outcomes, but it does not natively contain distinct local observables attached to spacetime regions whose algebra enforces relativistic separation.

In QFT, it does. Alice’s intervention is represented by a local operator $`{\widehat{O}}_{A}`$and Bob’s by a local operator $`{\widehat{O}}_{B}`$. If the regions are spacelike separated, the theory requires

``` math
\lbrack{\widehat{O}}_{A},{\widehat{O}}_{B}\rbrack = 0.
```

That means their order has no physical effect. Since different observers may disagree on which spacelike-separated event happened first, this is exactly what relativistic causality requires.

Poincaré transformations of spacetime are represented by unitary operators on the Hilbert or Fock space, and local fields transform accordingly. For a scalar field,

``` math
U(\Lambda,a)^{\dagger}\text{ }\widehat{\phi}(x)\text{ }U(\Lambda,a) = \widehat{\phi}\text{ }(\Lambda^{- 1}(x - a)).
```

This is the bridge connecting state space to spacetime. The relation holds because the field operator and the unitary Poincaré transformations are inherited from the same classical relativistic structure. The classical field already carries a covariant mode expansion and a Poincaré action on those modes. Quantization lifts that structure rather than replacing it: the mode coefficients become operators, and the classical symmetry generators become operators on Hilbert or Fock space. The unitary $`U(\Lambda,a)`$is built from those generators — not from the Hamiltonian alone, which gives only time translations — so its action on the field reproduces the same spacetime transformation law in operator form.

The state space must also be enlarged. Since the field may have no excitations, one excitation, two excitations, and so on, the state space must contain all of those sectors. This is “Fock space,” the direct sum of particle-number sectors:

``` math
\mathcal{F =}\mathbb{C} \oplus H_{1} \oplus H_{2} \oplus H_{3} \oplus \cdots\text{ }.
```

The vacuum sector $`\mathbb{C}`$ contains the zero-particle state. The sector $`H_{n}`$ contains the $`n`$-particle sector.



## Quantizing the Field

It is one thing to say that a quantum field is an operator attached to every point in space, obeying canonical commutation relations. We need to first construct a suitable field and then quantize it, or promote its values to operators. For a field to abide relativistic constraints, first, its values must be well-behaved under Lorentz transformations. This requires the values to be scalars, vectors, or spinors. Second, it must support transmitting signals are bounded by the speed of light. Before we get to nature’s actual quantum fields, we will work with a useful starting field called the Klein Gordon field. This is scalar valued, and it can be readily understood via a simple mechanical model. We will first construct a completely classical relativistic field and then promote its values to operators at which point we will see how quantum fields support particle creation.

### The Classical Model

We will construct the Klein-Gordon field using a model of a lattice of interconnected springs, and then take the limit of the that lattice spacing shrinking to the continuum limit, reflect on how such a model adheres to Relativity, and finally understand what it means to work in Fourier mode bases, which will become the momentum basis upon quantization.

#### The Spring Lattice Field Model

Let’s look at the mechanical model of this spring lattice. It may seem like we are being a bit obsessive about the details, but each element in the model plays a role in the properties particles have in QFT. The lattice we eventually want has 3 spatial dimensions, and at each node there is some value type. If that value is a scalar, we could represent the picture in 4 dimensions. Therefore if we, without loss of generality, reduce our spatial dimensions to one and let our field value use another, we can draw nice 2d pictures. We can start with a one-dimensional row of beads connected with springs, each bead constrained to slide up and down on a second spring connected to a base point.

\<picture\>

Call the vertical displacement of the $`n`$-th bead $`q_{n}(t)`$. Neighboring beads are connected by springs, so if one bead moves differently from its neighbors they pull it back toward them. In addition, each bead is attached to the fixed frame by its own local spring, so even if all the beads move together there is still a restoring force pulling each one back toward equilibrium.

That second ingredient matters. A chain with only neighbor springs supports waves, but its uniform mode costs no spring energy at all, because if every bead rises by the same amount no spring is stretched. The local spring changes that. It gives the uniform mode a nonzero oscillation frequency. That is the ingredient that will later become the mass scale of the field. There is something really subtle going on here that carries with it the relativistic structure of spacetime as manifest in the mass shell. Remember that the vertical dimension in our picture is spatial only for the purposes of drawing – it represents any scalar value. All spatial motion is contained in our horizontal dimension. Therefore, energy associated with uniform vertical oscillation is the energy when the system is at rest, which should sound familiar. It is structurally the same statement as $`E = mc^{2}`$. Recall that $`E = mc^{2}`$ is the rest case for the more general dispersion equation (setting $`c`$ to 1):

``` math
\ E^{2} = \ m^{2} + \ p^{2}
```

Looking ahead just a bit, once we derive the equation of motion for this lattice model, tune the propagation speed to $`c`$, and take the long-wavelength limit relative to the lattice spacing, we will find

``` math
\omega^{2} = \omega_{0}^{2} + c^{2}k^{2},
```

where $`\omega_{0}`$is the nonzero frequency of the uniform mode set by the local tether, matching the relativistic dispersion equation, and associating the rest frequency with math. If you are worried about units, one could look a bit farther ahead to the quantum energy-frequency relation and complete this equivalency with:

``` math
\left( \hslash\omega)^{2} = (\hslash\omega_{0})^{2} + c^{2}(\hslash k)^{2} \leftrightarrow E^{2} = m^{2}c^{4} + c^{2}p^{2}. \right.\ 
```

From this equation, we can read off the particle mass associated with the field:

``` math
m = \frac{\hslash\text{ }\omega_{0}}{c^{2}}
```

The natural classical Lagrangian for this lattice is

``` math
L = \sum_{n}^{}\left\lbrack \frac{1}{2}M{\dot{q}}_{n}^{\text{ }2} - \frac{1}{2}K_{0}q_{n}^{2} - \frac{1}{2}K(q_{n + 1} - q_{n})^{2} \right\rbrack.
```

Here $`M`$ is the mass of each bead, $`K`$is the spring constant coupling neighbors, and $`K_{0}`$is the spring constant of the local tether to the frame.

The terms have a simple interpretation. The first is kinetic energy. The middle term penalizes each bead for being away from zero, regardless of what the others are doing. The last penalizes neighboring beads for being at different heights. We can rewrite the Lagrangian in a way that is more idiomatic for fields by assigning each lattice site a position $`x_{n}`$and writing the site variable as a discrete field value,

``` math
q_{n}(t) \equiv \phi(x_{n},t),
```

so that

``` math
L = \sum_{n}^{}\left\lbrack \frac{1}{2}M\text{ }\dot{\phi}(x_{n},t)^{2} - \frac{1}{2}K_{0}\text{ }\phi(x_{n},t)^{2} - \frac{1}{2}K(\phi(x_{n + 1},t) - \phi(x_{n},t))^{2} \right\rbrack.
```

Using the standard procedure, the Euler–Lagrange equation of motion is hten:

``` math
M\ddot{\phi}(x_{n},t) + K_{0}\phi(x_{n},t) + K(2\phi(x_{n},t) - \phi(x_{n + 1},t) - \phi(x_{n - 1},t)) = 0.
```

This is the mechanical lattice analog of the field equation we are heading toward. The first term, $`M\ddot{\phi}`$, says the site value has inertia. The second term, $`K_{0}\phi`$, says the value itself is costly. Even a perfectly uniform displacement wants to relax back. The third term says the says mismatch between nearby sites is costly, so disturbances spread attempting to compensate for this cost.

We can define a new variable, $`\phi_{n} = \sqrt{M}\text{ }q_{n}`$, and rewrite the Lagrangian

``` math
L = \sum_{n}^{}\left\lbrack \frac{1}{2}{\dot{\phi}}_{n}^{\text{ }2} - \frac{1}{2}\frac{K_{0}}{M}\phi_{n}^{2} - \frac{1}{2}\frac{K}{M}(\phi_{n + 1} - \phi_{n})^{2} \right\rbrack,
```

and the equation of motion becomes

``` math
{\ddot{\phi}}_{n} - \frac{K}{M}(\phi_{n + 1} - 2\phi_{n} + \phi_{n - 1}) + \frac{K_{0}}{M}\phi_{n} = 0.
```

Now we have shifted the focus from mass and spring constants to frequency scales. The ratios

$`\Omega^{2} = \frac{K}{M},{\ \ \ \ \omega}_{0}^{2} = \frac{K_{0}}{M}`$

both have dimensions of inverse time squared. In this form the equation reads

``` math
{\ddot{\phi}}_{n} - \Omega^{2}(\phi_{n + 1} - 2\phi_{n} + \phi_{n - 1}) + \omega_{0}^{2}\phi_{n} = 0.
```

We can now look at its normal modes. If we try a “lattice plane wave" of the form

``` math
\phi_{n}(t) \propto e^{i(kna - \omega t)},
```

with $`a`$the lattice spacing, then substitution into the equation gives the lattice dispersion relation

``` math
\omega^{2} = \omega_{0}^{2} + 4\Omega^{2}{sin}^{2}\left( \frac{ka}{2} \right).
```

This equation nearly has the form of the dispersion equation we need. All that is left is to take the continuum limit that this lattice approximates at long wavelengths. For small $`ka`$,

``` math
\sin\left( \frac{ka}{2} \right) \approx \frac{ka}{2},
```

so that the dispersion relation becomes

``` math
\omega^{2} \approx \omega_{0}^{2} + \Omega^{2}a^{2}k^{2}.
```

This is the point at which the effective propagation speed emerges. Define

``` math
c^{2} = \Omega^{2}a^{2} = \frac{Ka^{2}}{M}.
```

Then the long-wavelength dispersion relation becomes, as promised,

``` math
\omega^{2} \approx \omega_{0}^{2} + c^{2}k^{2}.
```

Now let the lattice spacing go to zero while keeping the long-wavelength structure fixed. The discrete index $`n`$becomes a continuous position $`x`$, the discrete field $`\phi_{n}(t)`$becomes a continuous field $`\phi(x,t)`$, and the second difference becomes a spatial second derivative. The lattice equation turns into

``` math
\partial_{t}^{2}\phi - c^{2}\partial_{x}^{2}\phi + \omega_{0}^{2}\phi = 0.
```

In higher dimensions the same logic gives

``` math
\partial_{t}^{2}\phi - c^{2}\nabla^{2}\phi + \omega_{0}^{2}\phi = 0.
```

This is now a continuum classical field equation. And it is already very close to the relativistic form we want. The term with $`\nabla^{2}`$ came from the neighbor springs. The term with $`\omega_{0}^{2}`$ came from the local tether. The constant $`c`$ is no longer a spring-lattice parameter but the propagation speed of disturbances in the continuum limit. When we identify $`c`$ with the speed of light, we have completed building a model of a field that respects Lorentz symmetry.

Note that we are not merely making the claim that disturbances in the Klein Gordon field travel at finite speed. We are also making the more restrictive claim that their motion respects Lorentz transformations as the differential operator \<equation\> has the same Minkowski sign structure as the spacetime interval itself. That such an equation transforms properly under Lorentz in tantamount to any symmetry generator does so.

#### Comparing Klein Gordon and Schrödinger Equations

Let’s now look at the Klein Gordon and Schrodinger equations side by side and reflect on their differences.

Schrodinger: $`i\hslash\text{ }\partial_{t}\psi = - \frac{\hslash^{2}}{2m}\text{ }\partial_{x}^{2}\psi + V\psi`$*\*
Klein Gordon: $`\partial_{t}^{2}\phi - c^{2}\partial_{x}^{2}\phi + \omega_{0}^{2}\phi = 0.`$*\*

The Schrödinger equation is first order in time but second order in space. The Klein–Gordon, on the other hand, equation is second order in both. That second spatial derivative in the Schrödinger equation comes from the kinetic-energy term $`p^{2}/2m`$. In position space, $`p`$ becomes $`- i\hslash\partial_{x}`$, so $`p^{2}`$ becomes $`- \hslash^{2}\partial_{x}^{2}`$. This difference in the derivative structure places the two equations into different mathematical families. The Schrödinger equation belongs to the same broad class as diffusion equations, such as the heat equation. Such equations are extremely useful, and often physically accurate within their proper domain, but they have feature that, according to the diffusion equation, every other point is instantly affected, however slightly. The equation allows influence to leak outside any finite-speed causal cone, which is exactly our objection the Schrödinger equation. The Klein–Gordon equation behaves differently. Because time and space enter at the same differential order, it supports genuinely wave-like propagation. Disturbances travel at a finite characteristic speed. In the massless case that speed is exactly $`c`$. In the massive case the field still obeys a hyperbolic equation, so causal influence remains confined to the light cone even though individual wave packets need not move exactly at $`c`$.

We can gain insight into why an equation of the form of Klein Gordon requires finite speed propagation by examining classes of differential equations, which we can divide to hyperbolic, elliptic, and parabolic:

``` math
\boxed{\begin{matrix}
\text{Elliptic} & \partial_{t}^{2}\phi + c^{2}\partial_{x}^{2}\phi = 0 \\
\text{Parabolic} & \partial_{t}\phi - D\text{ }\partial_{x}^{2}\phi = 0 \\
\text{Hyperbolic} & \partial_{t}^{2}\phi - c^{2}\partial_{x}^{2}\phi = 0
\end{matrix}}
```

lliptic equations have second-derivative terms with the same sign. That is the same sign structure as Euclidean distance, where all squared directions add:

``` math
ds^{2} = dx^{2} + dy^{2} + \cdots
```

Nothing in that structure singles out a cone or a limiting speed. Accordingly, elliptic equations do not describe propagation from one event to another. They instead constrain a field over a region all at once. That is why they are the natural equations for static or steady-state configurations.

Parabolic equations introduce time evolution, but in an asymmetric way:

``` math
\partial_{t}\phi - D\text{ }\partial_{x}^{2}\phi = 0.
```

If we try a Fourier mode

``` math
\phi(x,t) \propto e^{i(kx - \omega t)},
```

then

``` math
- i\omega + Dk^{2} = 0,\text{so}\omega = - \text{ }iDk^{2}.
```

The frequency is imaginary rather than real, which means the mode does not oscillate. It decays:

``` math
\phi(x,t) \propto e^{ikx}e^{- Dk^{2}t}.
```

So parabolic equations smooth out differences instead of carrying traveling waves. A local disturbance spreads immediately, however weakly, to all distances. That is why diffusion equations do not respect a strict speed limit.

Hyperbolic equations have a mixed sign as the Minkowski metric does in hyperbolic spacetime.

``` math
\partial_{t}^{2}\phi - c^{2}\partial_{x}^{2}\phi = 0.
```

If we again try a plane wave *\*
``` math
\phi(x,t) \propto e^{ikx}e^{- Dk^{2}t}
```

we find

``` math
- \omega^{2} + c^{2}k^{2} = 0\  = > \ \omega^{2} = c^{2}k^{2}.
```

Now $`\omega`$ is real, so the solutions genuinely oscillate and propagate as waves. In fact, the operator factors:

``` math
\partial_{t}^{2} - c^{2}\partial_{x}^{2} = (\partial_{t} - c\partial_{x})(\partial_{t} + c\partial_{x}),
```

so disturbances move along

``` math
x \pm ct = \text{constant}.
```

That is finite-speed propagation.

This is exactly the structure relativity requires. The spacetime interval is

``` math
ds^{2} = - c^{2}dt^{2} + dx^{2}.
```

Because of the minus sign, the null condition

``` math
ds^{2} = 0
```

has nontrivial solutions:

``` math
dx = \pm c\text{ }dt.
```

These are the edges of the light cone. For a massive worldline,

``` math
d\tau^{2} = dt^{2} - \frac{dx^{2}}{c^{2}}
```

Thus, if $`dx/dt > c`$, then $`d\tau^{2} < 0`$ and proper time becomes imaginary. Physical worldlines must therefore remain inside or on the light cone.

The key point is that the operator

``` math
\partial_{t}^{2} - c^{2}\partial_{x}^{2}
```

has the same mixed-sign structure as the interval

``` math
- c^{2}dt^{2} + dx^{2}.
```

In spacetime, that structure produces a light cone. In the differential equation, it produces characteristic wave propagation at finite speed.

Elliptic equations have second-derivative terms with the same sign. That is the same sign structure as Euclidean distance, where all squared directions add:

``` math
ds^{2} = dx^{2} + dy^{2} + \cdots
```

Unlike the hyperbolic case, this structure does not produce a nontrivial null condition and so does not single out a characteristic cone or a finite propagation speed. Accordingly, elliptic equations do not describe propagation from one event to another. They instead constrain a field over a region all at once, which is why they are the natural equations for static or steady-state configurations.

Elliptic operators are Euclidean in sign structure, so they govern spatial balance; hyperbolic operators are Minkowskian in sign structure, so they govern causal propagation.

You may rightfully say at this point, ok, you’ve convinced me, the Klein Gordon field abides Relativity in a way that the Schrödinger equation does not, but we’ve done nothing to say the Klein Gordon field describes the evolution of quantum observables. That is exactly right. For now, we’re only saying that if we could use something like the Klein Gordon to describe quantum evolution, it would play well with Relativity.

This is also a good moment to look ahead. The Klein–Gordon equation is not itself the whole story of matter, and in fact no known fundamental matter field is a simple Klein–Gordon field. One might wonder whether the real secret of relativity is merely matching the order of time and space derivatives, and whether one could instead write an equation first order in both. That would be attractive, because first-order time evolution requires only one initial datum rather than two, which feels closer to ordinary quantum theory, where one specifies a state rather than both a value and its time derivative. The answer is yes, but only if the field has more structure than a scalar value at each point. A scalar field cannot support such an equation in a Lorentz-covariant way. But a spinor field can. That is exactly what happens in the Dirac equation, which is first order in both time and space and describes spin-$`\frac{1}{2}`$ particles such as electrons and quarks.

#### Working in the Momentum Basis

Before we leave our toy spring model, let's take the decisive step of switching to what will become the momentum basis and is for now the "normal mode," or "fourier mode" basis.

First, we need to understand the idea of diagonalizing an operator. As we know, an operator is a generalization of a matrix and diagonalizing a matrix – literally writing it in a form with only diagonal entries – is writing in a basis (the column vectors) of its eigenvectors so that its actions on those vectors is to scale them by their eigenvalues, but never to mix with other basis vectors. From this it follows that any vector written as a superposition of basis vectors transforms under the matrix by having its components scaled by the respective eigenvalues so that each component transforms independently. Looking ahead just a bit, we know that energy commutes with momentum (it can be written in terms of momentum), and we also know that energy is the time evolution generator, thus, if we write our systems Hamiltonian in term in the momentum basis, its components will evolve independently. This independence of evolution will determine how we talk about particle creation, annihilation, and count. We will build up a procedure in the decoupled momentum basis for which we have no equivalent in the coupled position basis.

Let’s hop down a level in detail and see what this looks like in our spring lattice. For the sake of simplicity, we will move to the massless case where this is simply once spring connecting each site. What we want to do is to describe an arbitrary vibrational pattern in terms of so-called independent normal modes. This is actually entirely concrete and in fact a common undergraduate classical mechanics problem used to illustrate the necessity of finding an eigenbasis, or decoupled basis, to solve mechanical problems. Let’s start by actually looking at some simple modes. Below are the k = 0, k=1, k=2 modes and then the k = (k=1) + (k=2) superposition mode.

<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image494.gif" style="width:6.5in;height:1.9875in" />

<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image495.gif" style="width:6.5in;height:1.9875in" />

<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image496.gif" style="width:6.5in;height:1.9875in" />

<figure>
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image497.gif" style="width:6.5in;height:2.06944in" />
<figcaption><p>Figure 67 - Example modes in spring lattice</p></figcaption>
</figure>

Now let’s actually solve this system.

Let the lattice have $`N`$sites, with one scalar degree of freedom $`\phi_{n}(t)`$at each site. The Lagrangian is

``` math
L = \sum_{n = 0}^{N - 1}\left\lbrack \frac{1}{2}{\dot{\phi}}_{n}^{2} - \frac{1}{2}m_{0}^{2}\phi_{n}^{2} - \frac{1}{2}\kappa(\phi_{n + 1} - \phi_{n})^{2} \right\rbrack,
```

with periodic boundary conditions, so $`\phi_{N} \equiv \phi_{0}`$. The first term is kinetic energy, the second is the onsite restoring term, and the third is the coupling between neighboring sites.

Applying the Euler–Lagrange equation to each $`\phi_{n}`$,

``` math
\frac{d}{dt}\frac{\partial L}{\partial{\dot{\phi}}_{n}} - \frac{\partial L}{\partial\phi_{n}} = 0,
```

gives

``` math
{\ddot{\phi}}_{n} + m_{0}^{2}\phi_{n} + \kappa(2\phi_{n} - \phi_{n + 1} - \phi_{n - 1}) = 0.
```

This is the system we want to solve. Written this way, it is in the site basis. The unknowns are the site values $`\phi_{n}(t)`$, and the equations are coupled because each site talks to its neighbors. To understand moving to the normal basis, let’s look at the Hamiltonian as this is the time generator.

The free lattice Hamiltonian is

``` math
H = \sum_{n}^{}\left\lbrack \frac{1}{2}{\dot{\phi}}_{n}^{\text{ }2} + \frac{1}{2}m_{0}^{2}\phi_{n}^{\text{ }2} + \frac{\kappa}{2}(\phi_{n + 1} - \phi_{n})^{2} \right\rbrack.
```

Here $`m_{0}`$sets the strength of the onsite restoring force, and $`\kappa`$sets the stiffness of the coupling between neighboring sites. In the site basis this Hamiltonian is not diagonal, because the last term ties each site to its neighbors.

What matters is that this coupling has the same form at every site. Shifting the whole lattice by one site leaves the Hamiltonian unchanged. The free lattice therefore has translation symmetry. To exploit that symmetry, we choose a basis of patterns that respond to a one-site shift as simply as possible. The discrete Fourier patterns do exactly that:

``` math
{e^{ikx_{n}} \rightarrow e}^{ika}e^{ikx_{n}}.
```

That is, as we have discussed earlier, plane waves, or equivalently here, normal modes, form an eigenbasis of the spatial translation operator. The entire complexity of each wave mode viewed in the position basis reduces to the eigenvalue $`k`$ in the mode basis.

Mathematically, we expand the site values, $`\phi_{0},\phi_{1},\ldots,\phi_{N - 1}`$, as

``` math
\phi_{n}(t) = \frac{1}{\sqrt{N}}\sum_{k}^{}q_{k}(t)e^{ikx_{n}},k = \frac{2\pi m}{Na},m = 0,1,\ldots,N - 1.
```
In the site basis, a configuration is a spatial pattern spread across all sites. In the Fourier basis, that same configuration is specified by the coefficients $`q_{k}(t)`$. The label $`k`$ tells us which translation-eigenpattern we mean. The coefficient $`q_{k}`$ tells us how much of that pattern is present. To use another visual analogy, a note on a guitar string has one characteristic shape, but the weight of that pattern oscillates with time:

<figure>
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image498.png" style="width:6.5in;height:1.59514in" />
<figcaption><p>Figure 68 - Mode oscillations (not position oscillations)</p></figcaption>
</figure>

Substituting this expansion into the equations of motion gives

``` math
{\ddot{q}}_{k} + \omega_{k}^{2}q_{k} = 0,\ \ \omega_{k}^{2} = m_{0}^{2} + 4\kappa{\sin}^{2}\left( \frac{ka}{2} \right).
```

Equivalently, the Hamiltonian becomes

``` math
H = \frac{1}{2}\sum_{k}^{}\left\lbrack p_{k}p_{- k} + \omega_{k}^{2}q_{k}q_{- k} \right\rbrack.
```

Thus, in the Fourier basis the Hamiltonian is diagonal in which the free lattice is written as a sum of independent oscillator energies, one for each allowed $`k`$.

We can see straight away that each independent equation of motion in the Fourier mode basis is simpler to solve than the coupled equation of motion in the position basis. But what really matters for us is that we have a procedure from fixed-particle quantum mechanics that quantizes energy levels in a harmonic oscillator. The fact that the field decomposes into decouple oscillators in the momentum basis will be the basis of the bridge from the field to particles. Whereas in fixed-particle quantum mechanics quantization of energy *for a* particle in a potential, in QFT energy quantization of the field *is a* particle.

# To-be-used-material

## Unitarity

Before introducing the full machinery of quantum mechanics, it is worth isolating one requirement that already tells us a great deal about what the theory must look like. If the basic object of the theory is not a point in phase space but a superposition of amplitudes, then its evolution cannot be arbitrary. It must preserve the structure that makes those amplitudes physically meaningful. That requirement is unitarity.

Let the state of a system be represented by a vector $`\mid \psi\rangle`$in a complex vector space equipped with an inner product $`\langle\phi \mid \psi\rangle`$. This inner product is not an ornamental extra. It is the structure from which the measurable content of the theory is built. Norms come from it. Overlaps come from it. Transition amplitudes come from it. Once probabilities are extracted from squared overlaps, the inner product becomes the quantity whose preservation matters.

An allowed time evolution must therefore preserve that inner product. If the state evolves by a linear map $`U`$, then the condition is

``` math
\langle U\phi \mid U\psi\rangle = \langle\phi \mid \psi\rangle
```

for all states $`\mid \phi\rangle`$and $`\mid \psi\rangle`$. A map with this property is called unitary. In operator form, this is

``` math
U^{\dagger}U = I.
```

That compact equation says a great deal. It says the evolution may rotate the state in its abstract space, it may mix components, it may alter phases, but it may not stretch, shrink, or scramble the geometry that gives the state physical meaning.

This geometry is richer than ordinary Euclidean geometry because the inner product is complex. If we temporarily view the complex vector space as a real one with extra structure, then the inner product splits into two parts,

``` math
\langle\phi \mid \psi\rangle = g(\phi,\psi) + i\text{ }\omega(\phi,\psi),
```

where

``` math
g(\phi,\psi) = Re\text{ }\langle\phi \mid \psi\rangle,\omega(\phi,\psi) = Im\text{ }\langle\phi \mid \psi\rangle.
```

The real part $`g`$plays the role of a metric-like structure. It measures lengths and angles. The imaginary part $`\omega`$is antisymmetric and area-like. It is the Hilbert-space remnant of the symplectic structure that classical mechanics preserves in phase space. In classical mechanics, lawful evolution preserves symplectic area. In quantum mechanics, lawful evolution preserves something stronger. It preserves the entire complex inner product, and therefore preserves both the metric-like and symplectic-like parts at once. Symplecticity has not disappeared. It has been absorbed into unitarity.

This is one reason quantum theory needs Hilbert space rather than ordinary configuration space. A wave-like state carries internal structure. Its components do not merely list mutually exclusive possibilities. They coexist with relative magnitudes and relative phases, and those relative phases affect future outcomes through interference. The state is therefore not just a distribution over alternatives. It is a single object whose parts can reinforce or cancel one another. A theory of such objects needs a geometry that can keep track of both size and phase relations. The complex inner product does exactly that.

Consider a state written as a superposition,

``` math
\mid \psi\rangle = \sum_{n}^{}c_{n} \mid n\rangle.
```

The coefficients $`c_{n}`$are amplitudes, not probabilities. Their squared magnitudes may eventually be read probabilistically in a suitable basis, but the state itself contains more than those magnitudes. It also contains the phase relations among the $`c_{n}`$. Those phases are not decorative. They are what make interference possible. Under unitary evolution,

``` math
\mid \psi(t)\rangle = U(t) \mid \psi(0)\rangle,
```

the amplitudes change, but they change in a way that preserves the full pattern of relations among components. A superposition may spread, twist, and recombine, but it does not come apart. The geometry that makes interference meaningful is carried forward intact.

From this one condition follow many of the most familiar features of quantum mechanics.

First, unitarity preserves norm. Since

``` math
\langle\psi(t) \mid \psi(t)\rangle = \langle\psi(0) \mid \psi(0)\rangle,
```

a normalized state remains normalized. This is why total probability is conserved in a closed quantum system. But probability conservation is only the most visible consequence, not the deepest one.

Second, unitarity preserves transition amplitudes and therefore transition probabilities. If two states have a given overlap now, they retain that overlap after both are evolved. The mutual relations among states are not distorted.

Third, unitarity preserves angles and orthogonality. If two states are orthogonal, meaning perfectly distinguishable in principle, then unitary evolution keeps them orthogonal. Quantum evolution may make a state harder for us to describe in everyday terms, but it does not erase the distinctions the theory itself makes. Distinguishability is preserved.

Fourth, unitarity makes closed-system evolution reversible. Since $`U^{\dagger}U = I`$, the inverse of $`U`$exists and is $`U^{\dagger}`$. One can run the evolution backward. This does not mean that every practical process in the world is reversible. Measurements, coarse-graining, and open-system effects complicate the story. But the underlying law for an isolated system does not discard information. It transforms without tearing.

These consequences are often taught separately. Probability conservation is presented in one place, reversibility in another, orthogonality in another. But they are all facets of the same geometric fact. A unitary evolution preserves the full inner-product structure of state space.

This gives quantum mechanics a kind of continuity very different from classical continuity. In classical mechanics, a system remains itself by tracing a path through phase space. In quantum mechanics, a state need not follow a sharp trajectory at all. It may be spread across many possibilities. It may evolve into a superposition whose components correspond to outcomes that classical language would regard as incompatible. Yet the state is not thereby destroyed into a formless cloud. What persists is not a point, but a structure. What survives is not certainty, but identity of form.

That is why unitarity deserves to be understood before the usual interpretive puzzles arrive. It tells us that quantum uncertainty is not chaos. Superposition does not mean that anything goes. The amplitudes evolve under a severe constraint. Their total geometric organization must be preserved. Norm is preserved. Distinguishability is preserved. Reversibility is preserved. The metric-like and symplectic-like aspects of the theory are preserved together.

Unitarity, then, is the principle that pulls identity out of the ashes of uncertainty. A quantum state may be indefinite with respect to many classical questions, but it is not without structure, and that structure is not allowed to decay under lawful evolution. The state may rotate through possibility, but it must remain itself.
