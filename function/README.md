# function
1.setdefault(key[, default]) 
    - 没有key，会添加key并且可以指定 一个默认值, 如果没有指定, 则认为是 None 返回, 如果指定了default, 则直接返回 default 值 
    - 有这个key,直接返回字典中对应的 key 的值 ,即使设置了default ,也不会返回default, 而是返回 key 对应的 value 值