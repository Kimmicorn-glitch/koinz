interface ProfileCardProps {
  name: string;
  township: string;
  skills: string[];
}

export function ProfileCard({ name, township, skills }: ProfileCardProps) {
  return (
    <article className="card p-6 animate-slideUp">
      <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-[#B11226] to-[#EE425E] mb-4" />
      <h3 className="text-lg font-semibold">{name}</h3>
      <p className="text-sm text-neutral-600">{township}</p>
      <div className="mt-3 flex flex-wrap gap-2">
        {skills.map((skill) => (
          <span key={skill} className="text-xs border border-[#f0c6ce] rounded-full px-2 py-1">
            {skill}
          </span>
        ))}
      </div>
    </article>
  );
}
