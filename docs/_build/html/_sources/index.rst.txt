CircularWood_4.0 Database API documentation
===========================================

This repository contains the **CircularWood_4.0 Database API**, developed as part of the Circular Wood 4.0 project at the **Robot Lab - Digital Production Research Group - Amsterdam University of Applied Science**.

Contact: j.jooshesh@hva.nl

The **CircularWood_4.0 API** supports a traceable, intelligent design-to-production workflow that minimizes material waste and optimizes manufacturing processes. The system allows for:

- Managing **wood inventory**, including type, dimensions, and availability.
- Storing **designs** created by users, where each design element is uniquely matched to materials in the inventory.
- Linking **designs to materials**, ensuring full traceability of which materials are used for which design and by which user.
- Storing **production** codes created from the nested designs to the materrials and linking that to the ID of the material
- Storing records of **production logs** linked to each design and material
- Traceability of the **environmental impact** of production from the circular wood usage



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   models
   resources
   workflow
   utils
   scripts


.. automodule:: resources
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: workflow
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: utils
   :members:
   :undoc-members:
   :show-inheritance:
