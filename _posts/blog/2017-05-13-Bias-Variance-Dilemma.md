---
layout: post
title: Understand Bias-Variance Dilemma with Intuition and Math
excerpt: "Mathematical derivation of bias-variance relationship"
modified: 2017-05-13T14:17:25-04:00
categories: blog
tags: [Machine Learning, Regression]
image:
  feature: site_logos/Logo Umbrella_Corporation.png
  credit: 
  creditlink: 
comments: true
share: true
---

<script type="text/x-mathjax-config">
 MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
</script>

### Preface

I was reading the book "Machine Learning - An Algorithmic Perspective" 2nd Ed by Stephen Marsland these days, and I came across the concept of "bias-variance dilemma" and its mathemical definition and derivations (page 36). Loosely speaking, if a model has few parameters to fit, it tends to have high bias and low variance, and if a model has a lot of parameters to fit, it tends to have low bias but high variance. High bias means that the model is to simple to reflect the complex nature of the phenomenon. High variance means that the model is over complicated to generalize and the parameters fit were very sensitive to the training data used. In reality, because data have noise, people were not able to achieve both perfect low bias and low variance. So people have to trade off between them. That is to say, people have to choose the right model to fit the data. I have known this concept long time ago, mostly from the introductions of several MOOC courses. But I have not delve into its mathematics to fully understand how it works.

![](/images/blog/2017-05-13-Bias-Variance-Dilemma/BiasVariance_illustration.pdf)

Unfortunately, although the book is overall a good book that covers most of fundamental knowledge of machine learning. It often has some minor mistakes in math. I also found there is mistakes in the derivation of the bias-variance relationship, and it is very confusing. So I tried to find these math on the world-wide web. Unfortunately, those materials are not perfect neither. Some of them looks good regarding the math, but they are too obscure and lack connectivity in the derivation from my point of view. Some of them provides good intuition and figures, but they are also having some math issues.

### Reading Materials

After doing multiple rounds of google searches, I think the combination of these two materials are the most easy to understand. I have annotated them in the pdf file for clarity. After reading both of them, I think you will fully understand what is bias and variance and their relashionships. This [stackflow answer](https://math.stackexchange.com/questions/676599/expected-value-of-an-expected-value) might also be helpful if you have some troubles reading the derivation. I personally do not recommend the Wikipedia one by the way, though it seems to be correct.

[Material 1](/downloads/blog/2017-05-13-Bias-Variance-Dilemma/BiasVariance_1.pdf)

It provides the figures to illustarte the origin of bias and variance, which other materials often lack. The derivation seems ok. However, it lacks one key clarification for the uncorrelatonship between two things therefore is not recommended as the rigorous derivation.

[Material 2](/downloads/blog/2017-05-13-Bias-Variance-Dilemma/BiasVariance_2.pdf)

It provides very detailed derivation step by step. Despite the minor math errors, it is the best one I have seen on the internet. I have already annotated the minor error and some basic statistics lemma/theorems if you cannot remember from the top of your head.