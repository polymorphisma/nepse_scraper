(module
  (table $_indirect_function_table (;0;) (export "_indirect_function_table") 2 2 funcref)
  (memory $memory (;0;) (export "memory") 256 256)
  (global $global0 (mut i32) (i32.const 66736))
  (elem $elem0 (i32.const 1) funcref (ref.func $_initialize))
  (func $_initialize (;0;) (export "_initialize")
    nop
  )
  (func $_rdx (;1;) (export "_rdx") (export "_cdx") (param $var0 i32) (param $var1 i32) (param $var2 i32) (param $var3 i32) (param $var4 i32) (result i32)
    local.get $var1
    i32.const 100
    i32.div_s
    i32.const 10
    i32.rem_s
    local.get $var1
    i32.const 10
    i32.div_s
    local.tee $var0
    i32.const 10
    i32.rem_s
    i32.add
    local.tee $var2
    local.get $var2
    local.get $var1
    local.get $var0
    i32.const 10
    i32.mul
    i32.sub
    i32.add
    i32.const 2
    i32.shl
    i32.const 1024
    i32.add
    i32.load
    i32.add
    i32.const 22
    i32.add
  )
  (func $cdx (;2;) (export "cdx") (param $var0 i32) (param $var1 i32) (param $var2 i32) (param $var3 i32) (param $var4 i32) (result i32)
    local.get $var1
    i32.const 10
    i32.div_s
    local.tee $var0
    i32.const 10
    i32.rem_s
    local.get $var1
    local.get $var0
    i32.const 10
    i32.mul
    i32.sub
    i32.add
    local.get $var1
    i32.const 100
    i32.div_s
    i32.const 10
    i32.rem_s
    i32.add
    i32.const 2
    i32.shl
    i32.const 1024
    i32.add
    i32.load
    i32.const 22
    i32.add
  )
  (func $rdx (;3;) (export "rdx") (param $var0 i32) (param $var1 i32) (param $var2 i32) (param $var3 i32) (param $var4 i32) (result i32)
    local.get $var1
    i32.const 100
    i32.div_s
    i32.const 10
    i32.rem_s
    local.get $var1
    i32.const 10
    i32.div_s
    local.tee $var0
    i32.const 10
    i32.rem_s
    i32.add
    local.tee $var2
    local.get $var2
    local.get $var1
    local.get $var0
    i32.const 10
    i32.mul
    i32.sub
    i32.add
    i32.const 2
    i32.shl
    i32.const 1024
    i32.add
    i32.load
    i32.add
    i32.const 32
    i32.add
  )
  (func $bdx (;4;) (export "bdx") (param $var0 i32) (param $var1 i32) (param $var2 i32) (param $var3 i32) (param $var4 i32) (result i32)
    local.get $var1
    i32.const 100
    i32.div_s
    i32.const 10
    i32.rem_s
    local.get $var1
    i32.const 10
    i32.div_s
    local.tee $var0
    i32.const 10
    i32.rem_s
    i32.add
    local.tee $var2
    local.get $var2
    local.get $var1
    local.get $var0
    i32.const 10
    i32.mul
    i32.sub
    i32.add
    i32.const 2
    i32.shl
    i32.const 1024
    i32.add
    i32.load
    i32.add
    i32.const 60
    i32.add
  )
  (func $ndx (;5;) (export "ndx") (param $var0 i32) (param $var1 i32) (param $var2 i32) (param $var3 i32) (param $var4 i32) (result i32)
    local.get $var1
    i32.const 10
    i32.div_s
    local.tee $var0
    i32.const 10
    i32.rem_s
    local.tee $var2
    local.get $var2
    local.get $var1
    local.get $var0
    i32.const 10
    i32.mul
    i32.sub
    i32.add
    local.get $var1
    i32.const 100
    i32.div_s
    i32.const 10
    i32.rem_s
    i32.add
    i32.const 2
    i32.shl
    i32.const 1024
    i32.add
    i32.load
    i32.add
    i32.const 88
    i32.add
  )
  (func $mdx (;6;) (export "mdx") (param $var0 i32) (param $var1 i32) (param $var2 i32) (param $var3 i32) (param $var4 i32) (result i32)
    local.get $var1
    i32.const 100
    i32.div_s
    i32.const 10
    i32.rem_s
    local.tee $var0
    local.get $var0
    local.get $var1
    i32.const 10
    i32.div_s
    local.tee $var2
    i32.const 10
    i32.rem_s
    local.get $var1
    local.get $var2
    i32.const 10
    i32.mul
    i32.sub
    i32.add
    i32.add
    i32.const 2
    i32.shl
    i32.const 1024
    i32.add
    i32.load
    i32.add
    i32.const 110
    i32.add
  )
  (func $stackSave (;7;) (export "stackSave") (result i32)
    global.get $global0
  )
  (func $stackRestore (;8;) (export "stackRestore") (param $var0 i32)
    local.get $var0
    global.set $global0
  )
  (func $stackAlloc (;9;) (export "stackAlloc") (param $var0 i32) (result i32)
    global.get $global0
    local.get $var0
    i32.sub
    i32.const -16
    i32.and
    local.tee $var0
    global.set $global0
    local.get $var0
  )
  (func $_errno_location (;10;) (export "_errno_location") (result i32)
    i32.const 1184
  )
  (data (i32.const 1024) "\05\00\00\00\08\00\00\00\04\00\00\00\07\00\00\00\09\00\00\00\04\00\00\00\06\00\00\00\09\00\00\00\05\00\00\00\05\00\00\00\06\00\00\00\05\00\00\00\03\00\00\00\05\00\00\00\04\00\00\00\04\00\00\00\09\00\00\00\06\00\00\00\06\00\00\00\08\00\00\00\08\00\00\00\06\00\00\00\08\00\00\00\06\00\00\00\05\00\00\00\08\00\00\00\04\00\00\00\09\00\00\00\05\00\00\00\09\00\00\00\08\00\00\00\05\00\00\00\03\00\00\00\04\00\00\00\07\00\00\00\07\00\00\00\04\00\00\00\07\00\00\00\03\00\00\00\09")
)