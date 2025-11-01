export default function Mascot({ className }) {
  return (
    <svg
      className={className}
      viewBox="0 0 180 180"
      role="img"
      aria-label="MindMate Mascot"
    >
      <defs>
        <radialGradient id="g1" cx="50%" cy="35%" r="70%">
          <stop offset="0%" stopColor="#BFD4FF" />
          <stop offset="60%" stopColor="#4C83FF" />
          <stop offset="100%" stopColor="#1E60FF" />
        </radialGradient>
      </defs>

      <circle cx="90" cy="105" r="50" fill="url(#g1)" />

      <circle cx="90" cy="65" r="42" fill="url(#g1)" />

      <rect
        x="85"
        y="18"
        width="10"
        height="20"
        rx="5"
        fill="url(#g1)"
      />
      <circle
        cx="90"
        cy="14"
        r="9"
        fill="url(#g1)"
      />

      <circle cx="75" cy="65" r="6" fill="#0F172A" />
      <circle cx="105" cy="65" r="6" fill="#0F172A" />
      <path
        d="M72 78c6 8 30 8 36 0"
        stroke="#0F172A"
        strokeWidth="4"
        strokeLinecap="round"
      />
    </svg>
  );
}
