{:ok, content} = File.read("input.txt")

# Part 1
{left, right} =
  content
  |> String.split("\n", trim: true)
  |> Enum.map(fn line ->
    [left, right] = String.split(line)
    {String.to_integer(left), String.to_integer(right)}
  end)
  |> Enum.unzip()

left = Enum.sort(left)
right = Enum.sort(right)

result1 =
  left
  |> Enum.zip(right)
  |> Enum.reduce(0, fn {a, b}, acc -> acc + abs(a - b) end)

IO.puts(result1)

# Part 2
freq = Enum.frequencies(right)

result2 =
  left
  |> Enum.reduce(0, fn a, acc -> acc + a * Map.get(freq, a, 0) end)

IO.puts(result2)
